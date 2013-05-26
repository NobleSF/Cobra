from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render, redirect
from apps.admin.controller.decorator import access_required

@access_required('seller')
def home(request, context={}):
  from apps.seller.models import Seller

  try:
    seller = Seller.objects.get(id=request.session['seller_id'])
    products = seller.product_set.all()
    context['seller'] = seller
    context['products'] = products
  except Exception as e:
    context = {'exception': e}

  return render(request, 'management/home.html', context)

@access_required('seller')
def orders(request):
  from apps.seller.models import Seller

  context = {}
  try:
    seller = Seller.objects.get(id=request.session['seller_id'])
    products = seller.product_set.all()
    context['seller'] = seller

  except Exception as e:
    context = {'exception': e}

  return render(request, 'management/orders.html', context)

@access_required('seller')
def catalog(request):
  from apps.seller.models import Seller

  context = {}
  try:
    seller = Seller.objects.get(id=request.session['seller_id'])
    products = seller.product_set.all()
    context['seller'] = seller

  except Exception as e:
    context = {'exception': e}

  return render(request, 'management/catalog.html', context)
