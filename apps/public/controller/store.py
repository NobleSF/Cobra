from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.template import RequestContext

def home(request, seller_id):
  from apps.seller.models import Seller, Asset, Product, Photo

  try:
    store = Seller.objects.get(id=seller_id)

    store.assets = Asset.objects.filter(seller=store).order_by('ilk')
    store.artisans = store.assets.filter(ilk='artisan')
    #store.utilities = store.assets.filter(ilk='tool') | store.assets.filter(ilk='material')

    products = store.product_set.all()
    for product in products:
      product.photos = product.photo_set.all()

    context = {'store':store, 'products':products}

  except Seller.DoesNotExist:
    return Http404

  except Exception as e:
    context = {'except':e}

  return render(request, 'store.html', context)
