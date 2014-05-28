from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from apps.admin.utils.exception_handling import ExceptionHandler
from django.views.decorators.cache import cache_page
from django.utils import timezone
from datetime import datetime
from apps.seller.models.product import Product
from apps.seller.models.photo import Photo
import json

def home(request, product_id, slug=None):
  product = get_object_or_404(Product, id=product_id)

  #permanent redirect when slug not included
  if product.slug and slug != product.slug:
    return redirect(product, permanent=True) #uses get_absolute_url

  return render(request, 'product.html', {'product': product})

def product(request): pass
"""
use django-rest to serve public product data
similar to the product_data feed already in use.



"""
