from django.http import Http404
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.utils import timezone
from settings.people import Tom
from apps.communication.controller.email_class import Email

def home(request, product_id):
  from apps.seller.models import Product, Photo
  from itertools import chain

  try:
    product = Product.objects.get(id=product_id)

    try: product.artisan = product.assets.filter(ilk='artisan')[0]#.order_by('?')[:1]
    except: pass
    product.materials = product.assets.filter(ilk='material')#.order_by('?')[:3]
    product.tools     = product.assets.filter(ilk='tool')#.order_by('?')[:3]
    product.utilities = list(chain(product.materials, product.tools))

    try:
      product.pinterest_url = ("http://www.pinterest.com/pin/create/button/" +
                               "?url=" + product.get_absolute_url() +
                               "&media=" + product.photo.original +
                               "&description=" + product.long_title)

    except: pass #if something here broke, it probably doesn't need to be working anyway

    more_products = (product.seller.product_set
                     .exclude(id=product.id)
                     .filter(sold_at=None)
                     .filter(approved_at__lte=timezone.now())
                     .filter(deactive_at=None)
                     .order_by('approved_at').reverse())

    context = {'product':       product,
               'more_products': more_products[:3]
              }

  except Product.DoesNotExist:
    raise Http404

  except Exception as e:
    Email(message="error on public product page: "+str(e)).sendTo(Tom.email)
    context = {'except':e}

  return render(request, 'product.html', context)

def collection(request, group, name=None):
  return render(request, 'collection.html',
    {'group':group}
  )
