from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext

def home(request, product_id):
  from seller.models import Product, Photo

  try:
    product = Product.objects.get(id=product_id)
    seller = product.seller

    product.photos = Photo.objects.filter(product=product).order_by('rank')
    for photo in product.photos:
      photo.feature_url = str(photo.thumb).replace('thumb','product')

    artisans  = product.assets.filter(ilk='artisan')
    tools     = product.assets.filter(ilk='tool')
    materials = product.assets.filter(ilk='material')

    context = {'product':product}

  except Exception as e:
    context = {'except':e}

  return render(request, 'product.html', context)

def collection(request, group, name=None):
  return render(request, 'collection.html',
    {'group':group}
  )
