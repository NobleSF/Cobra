import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from apps.admin.utils.decorator import access_required
from apps.admin.utils.exception_handling import ExceptionHandler
from apps.public.controller.cart_class import Cart
from apps.public.controller.forms import CartForm
from apps.public.models.checkout import Checkout
from apps.seller.models.product import Product

def get_or_none(model, **kwargs):
  try:
    return model.objects.get(**kwargs)
  except model.DoesNotExist:
    return None

def cart(request):
  try:
    cart, created = Cart.objects.get_or_create(id=request.session.get('cart_id'))
  except Exception as e:
    ExceptionHandler(e, "error on cart")
    cart = Cart()

  if cart.checked_out: #if paid, start a new empty cart
    cart = Cart()

  cart.save()
  request.session['cart_id'] = cart.id

  cart_form = CartForm()
  try:
    for field_name in ['email', 'name', 'address1', 'address2', 'city',
                       'state', 'postal_code', 'country', 'notes', 'receipt']:
      cart_form.fields[field_name].initial = cart.getData(field_name)
  except Exception as e:
    ExceptionHandler(e, "error on cart form")

  context = {'cart': cart, 'cart_form': cart_form}

  if 'admin_id' in request.session:
    cart.getAnouCheckoutId()
  else:
    from settings.settings import STRIPE_PUBLIC_KEY
    context['STRIPE_PUBLIC_KEY'] = STRIPE_PUBLIC_KEY

  return render(request, 'checkout/cart.html', context)

def cartAdd(request, product_id):
  cart, created = Cart.objects.get_or_create(id=request.session.get('cart_id'))

  try:
    cart.addItem(Product.objects.get(id=product_id))

  except Exception as e:
    ExceptionHandler(e, "in checkout.cartAdd")
    #return to where you came from
    if 'HTTP_REFERER' in request.META:
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

  finally:
    request.session['cart_id'] = cart.id
    return redirect('cart')

def cartRemove(request, product_id):
  cart, created = Cart.objects.get_or_create(id=request.session.get('cart_id'))

  if not created:
    try:
      cart.removeItem(Product.objects.get(id=product_id))
    except Exception as e:
      ExceptionHandler(e, "in checkout.cartRemove")

  return redirect('cart')

def cartSave(request): #ajax requests only
  if request.method == 'GET': # it must be an ajax GET to work
    cart = Cart(request)
    cart.saveData(request.GET.get('name'), request.GET.get('value'))
    response = {'success': str(request.GET.get('name'))+" saved"}
  else:
    response = {'problem': "not GET"}

  return HttpResponse(json.dumps(response), content_type='application/json')

@csrf_exempt
def stripe_checkout(request):
  import stripe
  from settings.settings import STRIPE_SECRET_KEY

  stripe_token = request.POST.get('stripeToken')
  #stripe_token_type = request.POST.get('stripeTokenType')
  #stripe_email = request.POST.get('stripeEmail')
  stripe.api_key = STRIPE_SECRET_KEY #initiate stripe

  checkout = Checkout(cart_id=request.session.get('cart_id'))
  if stripe_token:
    try:
      charge = stripe.Charge.create(
          amount=int(float(cart.summary()) * 100), # amount in cents, again
          currency="usd",
          card=stripe_token,
          description="payment to Anou"
      )
      checkout.payment_id = charge.get('id')
      checkout.checkout_data = charge

    except stripe.CardError, e:
      # The card has been declined
      print "card has been declined"
    except Exception as e:
      ExceptionHandler(e, 'in checkout.stripe_checkout')

  checkout.save()
  return redirect('confirmation', checkout.public_id)

def confirmation(request, checkout_id=None):
  from apps.public.controller.order_class import getOrders

  checkout_id = checkout_id or request.GET.get('checkout_id')
  checkout = Checkout.objects.get(payment_id=checkout_id)

  if checkout.cart.wepay_checkout_id:
    new_payment_data = checkout.getWepayCheckoutData() #return {} if no data available
    if new_payment_data:
      checkout.payment_data = new_payment_data

  if not checkout.payment_data: #empty data means no checkout_id created for the payment.
    checkout_data = {'problem': "No order exists with that confirmation number (checkout_id)"}

  else:
    #at this point we know that the order is real
    data = checkout.payment_data
    try:
      #if necessary, remove from session and checkout the cart
      if( data.get('gross') and
          data.get('state') in ['authorized', 'reserved', 'captured', 'refunded']
      ) or (
        data.get('manual_order')
      ) or (
        data.get('paid')
      ):
        # checkout.is_paid = True
        # checkout.save()#orders will be created if necessary

        if request.session.get('cart_id') and checkout.cart.id == request.session.get('cart_id'):
          del request.session['cart_id']

        if data.get('state') in ['refunded'] or data.get('refunded'):
          data['refund'] = True
      else:
        data = {'problem': "Payment on order is not complete."}

    except Exception as e:
      ExceptionHandler(e, "in checkout.confirmation")
      data = {'error': "Problem collecting your order information.",
                       'exception': e
                       }
      #todo: email the customer that we are aware of the problem

  context = {'cart':checkout.cart, 'checkout_data':data}
  try: context['orders'] = orders #if the variable exists
  except: pass

  return render(request, 'checkout/confirmation.html', context)

@access_required('admin')
def adminCheckout(request): #ajax requests only
  from django.core.urlresolvers import reverse
  from apps.communication.controller.email_class import Email
  from settings.people import Dan, Tifawt

  cart, created = Cart.objects.get_or_create(id=request.session.get('cart_id'))

  if not (cart.checkout.contact and cart.checkout.shipping_address and cart.checkout.notes):
    raise Exception("Missing complete shipping address or notes")

    reverse('confirmation', args=[cart.checkout.public_id])
    confirmation_url = request.build_absolute_uri(confirmation)
    confirmation_html_link = "<a href='%s'>%s</a>" % (confirmation_url, confirmation_url)
    message = "<p>To complete manual checkout go to: "+confirmation_html_link+"</p>"
    Email(message=message).sendTo([Dan.email,Tifawt.email]) #only send to trusted staff

  return HttpResponse(json.dumps({'email':'sent'}), content_type='application/json', status='200')
