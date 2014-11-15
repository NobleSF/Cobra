import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from apps.admin.utils.decorator import access_required
from apps.admin.utils.exception_handling import ExceptionHandler
from apps.public.controller.cart_class import Cart
from apps.public.controller.forms import CartForm
from apps.seller.models.product import Product

def cart(request):
  cart = Cart(request)

  #if the cart is already checked out, make a new cart
  if cart.cart.checked_out:
    del request.session['cart_id']
    cart = Cart(request)

  cart_form = CartForm()
  try:
    for field_name in ['email', 'name', 'address1', 'address2', 'city',
                       'state', 'postal_code', 'country', 'notes', 'receipt']:
      cart_form.fields[field_name].initial = cart.getData(field_name)
  except:
    pass

  context = {'cart': cart, 'cart_form': cart_form}

  if 'admin_id' in request.session:
    cart.getAnouCheckoutId()
  else:
    from settings.settings import STRIPE_PUBLIC_KEY
    context['STRIPE_PUBLIC_KEY'] = STRIPE_PUBLIC_KEY

  return render(request, 'checkout/cart.html', context)

def cartAdd(request, product_id):
  cart = Cart(request)

  try:
    cart.add(Product.objects.get(id=product_id))
    return redirect('cart')

  except Exception as e:
    ExceptionHandler(e, "in checkout.cartAdd")
    if 'HTTP_REFERER' in request.META:
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
      return redirect('cart')

def cartRemove(request, product_id):
  cart = Cart(request)

  try:
    cart.remove(Product.objects.get(id=product_id))
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
  stripe.api_key = STRIPE_SECRET_KEY

  #stripe_token_type = request.POST.get('stripeTokenType')
  #stripe_email = request.POST.get('stripeEmail')

  cart = Cart(request)

  try:
    charge = stripe.Charge.create(
        amount=int(float(cart.summary()) * 100), # amount in cents, again
        currency="usd",
        card=stripe_token,
        description="payment to Anou"
    )
    cart.cart.stripe_charge_id = charge.get('id')
    cart.cart.wepay_checkout_id = None
    cart.cart.checkout_data = charge
    cart.cart.save()

  except stripe.CardError, e:
    # The card has been declined
    print "card has been declined"
  except Exception as e:
    print str(e)

  return redirect('confirmation', cart.cart.checkout_id)

def confirmation(request, checkout_id=None):
  from apps.public.controller.order_class import getOrders

  checkout_id = checkout_id or request.GET.get('checkout_id')
  print checkout_id
  cart = Cart(request, checkout_id)

  checkout_data = cart.getCheckoutData() #return {} if no data available
  #print checkout_data
  #also runs checkout processes if necessary

  if not checkout_data: #empty data means no checkout_id created for the cart.
    checkout_data = {'problem': "No order exists with that confirmation number (checkout_id)"}

  else:
    #at this point we know that the order is real
    try:
      #if necessary, remove from session and checkout the cart
      if( checkout_data.get('gross') and
          checkout_data.get('state') in ['authorized', 'reserved', 'captured', 'refunded']
      ) or (
        checkout_data.get('manual_order')
      ) or (
        checkout_data.get('paid')
      ):
        if cart.count: #if there are things in the cart
          cart.checkout()
          orders = getOrders(checkout_id) #must run after cart.checkout()

        if request.session.get('cart_id') and cart.cart.id == request.session.get('cart_id'):
          del request.session['cart_id']

        if checkout_data.get('state') in ['refunded'] or checkout_data.get('refunded'):
          checkout_data['refund'] = True
      else:
        checkout_data = {'problem': "Payment on order is not complete."}

    except Exception as e:
      ExceptionHandler(e, "in checkout.confirmation")
      checkout_data = {'error': "Problem collecting your order information.",
                       'exception': e
                       }
      #todo: email the customer that we are aware of the problem

  context = {'cart':cart, 'checkout_data':checkout_data}
  try: context['orders'] = orders #if the variable exists
  except: pass

  return render(request, 'checkout/confirmation.html', context)

@access_required('admin')
def adminCheckout(request): #ajax requests only
  from django.core.urlresolvers import reverse
  from apps.communication.controller.email_class import Email
  from settings.people import Dan, Tifawt

  try:
    cart = Cart(request)

    if not (cart.contact and cart.shipping_address and cart.notes):
      raise Exception("Missing complete shipping address or notes")

    confirmation = reverse('confirmation')+'?checkout_id='+cart.cart.anou_checkout_id
    confirmation_url = request.build_absolute_uri(confirmation)
    confirmation_html_link = "<a href='%s'>%s</a>" % (confirmation_url, confirmation_url)
    message = "<p>To complete manual checkout go to: "+confirmation_html_link+"</p>"
    Email(message=message).sendTo([Dan.email,Tifawt.email]) #only send to trusted staff

  except Exception as e:
    ExceptionHandler(e, "in checkout.adminCheckout")
    responseObject = HttpResponse(content=json.dumps({'error':str(e)}),
                                  content_type='application/json',
                                  status='500')
  else:
    responseObject = HttpResponse(json.dumps({'email':'sent'}),
                                  content_type='application/json',
                                  status='200')
  finally:
    return responseObject

def custom_order(request):
  return render(request, 'checkout/custom_order.html')
