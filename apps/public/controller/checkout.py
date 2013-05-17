from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.utils import simplejson

from apps.public.controller.cart_class import Cart
from apps.public.controller.forms import CartForm

def cart(request):
  cart = Cart(request)
  total = cart.summary()
  context = {'cart':Cart(request), 'cart_form':CartForm()}
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

def confirmation(request):
  return render(request, 'checkout/confirmation.html')

def custom_order(request):
  return render(request, 'checkout/custom_order.html')
