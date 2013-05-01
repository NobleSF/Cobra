from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.utils import simplejson

def cartAdd(request, product_id):
  from seller.models import Product

  try:
    product = Product.objects.get(id=product_id)

    if 'cart' in request.session:
      request.session['cart'].products.append(product.id)
    else:
      request.session['order_id'] = Cart()

    return redirect('cart')

  except Exception as e:
    context = {'except':e}
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

def cart(request, product_id=None):

  return render(request, 'checkout/cart.html')

def payment(request):
  return render(request, 'checkout/payment.html')

def confirmation(request):
  return render(request, 'checkout/confirmation.html')

def custom_order(request):
  return render(request, 'checkout/custom_order.html')
