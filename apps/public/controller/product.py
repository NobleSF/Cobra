from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext

def home(request, product_id):
  from apps.seller.models import Product, Photo
  from itertools import chain

  try:
    #product = get_object_or_404(Product, id=product_id)
    product = Product.objects.get(id=product_id)

    product.photos = product.photo_set.order_by('rank')
    for photo in product.photos:
      photo.feature_url = photo.product

    product.artisan   = product.assets.filter(ilk='artisan')[0]#.order_by('?')[:1]
    product.materials = product.assets.filter(ilk='material')#.order_by('?')[:3]
    product.tools     = product.assets.filter(ilk='tool')#.order_by('?')[:3]
    product.utilities = list(chain(product.materials, product.tools))

    more_products = product.seller.product_set.exclude(id=product.id)[:8]

    context = {'product':       product,
               'more_products': more_products
              }

  except Product.DoesNotExist:
    raise Http404

  except Exception as e:
    context = {'except':e}

  return render(request, 'product.html', context)

def collection(request, group, name=None):
  return render(request, 'collection.html',
    {'group':group}
  )
