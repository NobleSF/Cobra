from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.utils import simplejson
from django.contrib import messages

from apps.public.controller.cart_class import Cart
from apps.public.controller.forms import CartForm

def cart(request):
  cart = Cart(request)
  cart_form = CartForm()
  try:
    cart_form.fields['email'].initial = cart.getData('email')
    cart_form.fields['name'].initial  = cart.getData('name')
  except Exception as e:
    pass
  finally:
    context = {'cart':cart, 'cart_form':cart_form}

  if cart.count():
    wepay_checkout_uri = cart.getWePayCheckoutURI()
    if not str(wepay_checkout_uri).startswith("http"):
      context['exception'] = wepay_checkout_uri
      messages.warning(request, 'WePay connection issue. You are unable to checkout.')
    else:
      context['wepay_checkout_uri'] = wepay_checkout_uri

  return render(request, 'checkout/cart.html', context)

def cartAdd(request, product_id):
  from apps.seller.models import Product
  cart = Cart(request)
  try:
    product = Product.objects.get(id=product_id)
  except Exception as e:
    context = {'problem':"Received bad product id"}
    return HttpResponseRedirect(request.META["HTTP_REFERER"], context)
  else:
    cart.add(product)
    context = {'success':"added product to cart"}
    return redirect('cart')

def cartRemove(request, product_id):
  from apps.seller.models import Product
  cart = Cart(request)
  try:
    product = Product.objects.get(id=product_id)
  except Exception as e:
    context = {'problem':"Received bad product id"}
    return HttpResponseRedirect(request.META["HTTP_REFERER"], context)
  else:
    cart.remove(product)
    context = {'success':"removed product from cart"}
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

  return HttpResponse(simplejson.dumps(response), mimetype='application/json')

def confirmation(request):
  from apps.public.controller.order_class import getOrders
  checkout_id = None

  try:
    if request.method == 'GET':
      checkout_id = request.GET.get('checkout_id')
  except:
    pass # no worries, use the checkout_id from the session cart
  finally:
    #Cart() creates a new cart if checkout_id=None and no cart in request.session
    cart = Cart(request, checkout_id)
    checkout_data = cart.getCheckoutData() #return {} if no data available
    #also runs checkout processes if necessary

  if not checkout_data: #empty data means no checkout_id created for the cart.
    checkout_data = {'problem': "No order exists with that confirmation number (checkout_id)"}

  else:
    #at this point we know that the order is real
    try:
      #if necessary, remove from session and checkout the cart
      if checkout_data.get('gross') and \
         checkout_data.get('state') in ['authorized', 'reserved', 'captured']:
        cart.checkout()
        orders = getOrders(checkout_id)
        try: del request.session['cart_id']
        except: pass
      else:
        checkout_data = {'problem': "Payment on order is not complete."}

    except Exception as e:
      checkout_data = {'error': "Problem collecting your order information.",
                       'exception': e
                       }
      #email Tom and CC the customer

  context = {'cart':cart, 'checkout_data':checkout_data}
  try: context['orders'] = orders #if the variable exists
  except: pass

  return render(request, 'checkout/confirmation.html', context)

def custom_order(request):
  return render(request, 'checkout/custom_order.html')
