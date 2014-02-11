from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from apps.admin.utils.decorator import access_required
from apps.admin.utils.exception_handling import ExceptionHandler
import json
from django.contrib import messages

from apps.public.controller.cart_class import Cart
from apps.public.controller.forms import CartForm

def cart(request):
  cart = Cart(request)

  #if the cart is already checked out, make a new cart
  if cart.cart.checked_out:
    del request.session['cart_id']
    cart = Cart(request)

  cart_form = CartForm()
  try:
    cart_form.fields['email'].initial = cart.getData('email')
    cart_form.fields['name'].initial  = cart.getData('name')
  except: pass
  finally:
    context = {'cart':cart, 'cart_form':cart_form}

  if 'admin_id' in request.session:
    anou_checkout_id = cart.getAnouCheckoutId()
    if not isinstance(anou_checkout_id, basestring):
      messages.warning(request, 'You are unable to checkout.')

  elif cart.count():
    wepay_checkout_uri = cart.getWePayCheckoutURI()
    if not isinstance(wepay_checkout_uri, basestring):
      context['exception'] = str(wepay_checkout_uri)
      messages.warning(request, 'WePay connection issue. You are unable to checkout.')
    else:
      context['wepay_checkout_uri'] = wepay_checkout_uri

  return render(request, 'checkout/cart.html', context)

def cartAdd(request, product_id):
  from apps.seller.models import Product
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
  from apps.seller.models import Product
  cart = Cart(request)

  try:
    cart.remove(Product.objects.get(id=product_id))
    return redirect('cart')

  except Exception as e:
    ExceptionHandler(e, "in checkout.cartRemove")
    if 'HTTP_REFERER' in request.META:
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
      return redirect('cart')

def cartSave(request): #ajax requests only
  if request.method == 'GET': # it must be an ajax GET to work
    try:
      cart = Cart(request)
      cart.saveData(request.GET['name'], request.GET['value'])
      response = {'success':request.GET['name']+" saved"}

    except Exception as e:
      response = {'exception': e}

  else:
    response = {'problem':"not GET"}

  return HttpResponse(json.dumps(response), content_type='application/json')

def confirmation(request):
  from apps.public.controller.order_class import getOrders
  checkout_id = None

  try:
    if request.method == 'GET':
      checkout_id = request.GET.get('checkout_id')
  except:
    #if an admin is logged in, they should not have come without a checkout_id
    if 'admin_id' in request.session:
      raise Exception("No checkout_id provided. checkout_id is required for admins")
    else:
      pass # no worries, use the checkout_id from the session cart
  finally:
    cart = Cart(request, checkout_id)

  checkout_data = cart.getCheckoutData() #return {} if no data available
  #also runs checkout processes if necessary

  if not checkout_data: #empty data means no checkout_id created for the cart.
    checkout_data = {'problem': "No order exists with that confirmation number (checkout_id)"}

  else:
    #at this point we know that the order is real
    try:
      #if necessary, remove from session and checkout the cart
      if( checkout_data.get('gross') and
          checkout_data.get('state') in ['authorized', 'reserved', 'captured']
      ) or (
          checkout_data.get('manual_order')
      ):
        if cart.count: #if there are things in the cart
          cart.checkout()
          orders = getOrders(checkout_id) #must run after cart.checkout()

        if request.session.get('cart_id') and cart.cart.id == request.session.get('cart_id'):
          del request.session['cart_id']
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
  from settings.people import Dan

  try:
    cart = Cart(request)

    if not (cart.contact and cart.shipping_address and cart.notes):
      raise Exception("Missing complete shipping address or notes")

    confirmation = reverse('confirmation')+'?checkout_id='+cart.cart.anou_checkout_id
    confirmation_url = request.build_absolute_uri(confirmation)
    confirmation_html_link = "<a href='%s'>%s</a>" % (confirmation_url, confirmation_url)
    message = "<p>To complete manual checkout go to: "+confirmation_html_link+"</p>"
    Email(message=message).sendTo(Dan.email)

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
