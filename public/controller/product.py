from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext

def home(request, product_id):
  from seller.models import Product, Photo
  from itertools import chain

  try:
    #product = get_object_or_404(Product, id=product_id)
    product = Product.objects.get(id=product_id)

    product.photos = Photo.objects.filter(product=product).order_by('rank')
    for photo in product.photos:
      photo.feature_url = str(photo.thumb).replace('thumb','product')

    product.artisans  = product.assets.filter(ilk='artisan').order_by('?')[:1]
    product.materials = product.assets.filter(ilk='material').order_by('?')[:3]
    product.tools     = product.assets.filter(ilk='tool').order_by('?')[:3]
    product.utilities = list(chain(product.materials, product.tools))

    product.utilities_bootstrap_span_length = int(12/len(product.utilities))

    context = {'product':product}

  except Product.DoesNotExist:
    raise Http404

  except Exception as e:
    context = {'except':e}

  return render(request, 'product.html', context)

def collection(request, group, name=None):
  return render(request, 'collection.html',
    {'group':group}
  )
