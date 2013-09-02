from django.http import Http404
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from datetime import datetime

def home(request, product_id):
  from apps.seller.models import Product, Photo
  from itertools import chain

  try:
    product = Product.objects.get(id=product_id)

    product.photos = product.photo_set.order_by('rank')
    for photo in product.photos:
      photo.feature_url = photo.product

    try: product.artisan = product.assets.filter(ilk='artisan')[0]#.order_by('?')[:1]
    except: pass
    product.materials = product.assets.filter(ilk='material')#.order_by('?')[:3]
    product.tools     = product.assets.filter(ilk='tool')#.order_by('?')[:3]
    product.utilities = list(chain(product.materials, product.tools))

    seller_products   = product.seller.product_set.exclude(id=product.id)
    unsold_products   = seller_products.filter(sold_at=None)
    approved_products = unsold_products.filter(approved_at__lte=datetime.today())
    active_products   = approved_products.filter(deactive_at=None)
    ordered_products  = active_products.order_by('approved_at').reverse()

    context = {'product':       product,
               'more_products': ordered_products[:3]
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
