from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.utils import simplejson

from apps.public.controller.cart_class import Cart
from apps.public.controller.forms import CartForm

def cart(request):
  cart = Cart(request)
  total = cart.summary()
  cart_form = CartForm()
  try:
    cart_form.fields['email'].initial       = cart.getData('email')
    cart_form.fields['name'].initial        = cart.getData('name')
    cart_form.fields['address1'].initial    = cart.getData('address1')
    cart_form.fields['address2'].initial    = cart.getData('address2')
    cart_form.fields['city'].initial        = cart.getData('city')
    cart_form.fields['state'].initial       = cart.getData('state')
    cart_form.fields['postal_code'].initial = cart.getData('postal_code')
    cart_form.fields['country'].initial     = cart.getData('country')
  except Exception as e:
    pass

  context = {'cart':Cart(request), 'cart_form':cart_form}
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
  #from apps.public.controller.order_class import Order
  cart = Cart(request)
  orders = []
  for item in cart:
    orders.append(Order(item, cart))

  cart.checkout()
  context = {'cart':cart}
  return render(request, 'checkout/confirmation.html', context)

def custom_order(request):
  return render(request, 'checkout/custom_order.html')
