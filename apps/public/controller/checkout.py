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
      context = {'success':request.GET['name']+" saved"}

    except Exception as e:
      context = {'exception': e}

  else:
    context = {'problem':"not GET"}

  response = context
  return HttpResponse(simplejson.dumps(response), mimetype='application/json')

def confirmation(request):
  from apps.public.controller.order_class import Order

  checkout_id = None
  try:
    if request.method == 'GET':
      checkout_id = request.GET.get('checkout_id')
  except: pass
  #will use the checkout_id from the session cart, if not provided
  finally:
    cart = Cart(request, checkout_id)

  checkout_data = Order.getCheckoutData(cart)

  context = {'cart':cart, 'checkout_data':checkout_data}
  return render(request, 'checkout/confirmation.html', context)

def custom_order(request):
  return render(request, 'checkout/custom_order.html')
