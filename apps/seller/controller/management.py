from django.http import HttpResponse
from django.utils import simplejson, timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.admin.controller.decorator import access_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from settings.people import Tom
from apps.communication.controller.email_class import Email

@access_required('seller')
def home(request):
  from apps.seller.models import Seller

  try:
    seller = Seller.objects.get(id=request.session['seller_id'])
    context = {'seller': seller}
  except Exception as e:
    Email(message="error on seller home: "+str(e)).sendTo(Tom.email)
    context = {'exception': e}

  return render(request, 'management/home.html', context)

@access_required('seller')
def products(request):
  from apps.seller.models import Seller

  try:
    seller = Seller.objects.get(id=request.session['seller_id'])
    products = (seller.product_set.filter(active_at__lte=timezone.now(),
                                          deactive_at=None,
                                          sold_at=None)
                                  .filter(
                                          Q(approved_at__lte=timezone.now()) |
                                          Q(in_holding=True)
                                  ))


    context = {'seller': seller, 'products': products}
  except Exception as e:
    Email(message="error on seller products page: "+str(e)).sendTo(Tom.email)
    context = {'exception': e}

  return render(request, 'management/products.html', context)

@access_required('seller')
def orders(request):
  from apps.seller.models import Seller

  try:
    seller = Seller.objects.get(id=request.session['seller_id'])
    sold_products = seller.product_set.filter(sold_at__lte=timezone.now())
    for product in sold_products:
      product.order = product.order_set.all()[0]
    context = {'seller': seller, 'products': sold_products}

  except Exception as e:
    Email(message="error on seller orders page: "+str(e)).sendTo(Tom.email)
    context = {'exception': e}

  return render(request, 'management/orders.html', context)
