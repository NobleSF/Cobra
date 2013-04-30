from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext

def home(request, seller_id):
  from seller.models import Seller, Asset, Product, Photo

  #try:
  store = Seller.objects.get(id=seller_id)

  store.assets = Asset.objects.filter(seller=store).order_by('ilk')
  store.artisans = store.assets.filter(ilk='artisan')
  store.utilities = store.assets.filter(ilk='tool') | store.assets.filter(ilk='material')

  products = Product.objects.filter(seller=store)
  for product in products:
    product.name = product.assets.filter(ilk='product')[0].name
    product.main_photo = Photo.objects.filter(product=product)[0].thumb
    product.extra_photos = Photo.objects.filter(product=product)[1:4]

  context = {'store':store, 'products':products}

  #except Exception as e:
  #  context = {'except':e}

  return render(request, 'store.html', context)
