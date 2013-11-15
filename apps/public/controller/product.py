from django.http import HttpResponse, Http404
from django.shortcuts import render
from apps.admin.utils.exception_handling import ExceptionHandler
from django.views.decorators.cache import cache_page
from django.utils import timezone
from apps.seller.models import Product, Photo
from itertools import chain
from django.utils import simplejson as json

def home(request, product_id, slug=None):
  try:
    product = Product.objects.get(id=product_id)

    try: product.artisan = product.assets.filter(ilk='artisan')[0]#.order_by('?')[:1]
    except: pass
    product.materials = product.assets.filter(ilk='material')#.order_by('?')[:3]
    product.tools     = product.assets.filter(ilk='tool')#.order_by('?')[:3]
    product.utilities = list(chain(product.materials, product.tools))

    try:
      product.pinterest_url = ("http://www.pinterest.com/pin/create/button/" +
                               "?url=http://www.theanou.com" + product.get_absolute_url() +
                               "&media=" + product.photo.original +
                               "&description=" + product.title_description)

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
    ExceptionHandler(e, "in product.home")
    context = {'exception', str(e)}

  return render(request, 'product.html', context)

@cache_page(172800) #cache for 48 hours
def product_data(request=None, version=1):
  from django.utils import timezone
  product_amalgam_bomb = []

  for product in Product.objects.filter(approved_at__lte=timezone.now()):

    product_data = {
      'id':                     product.id,
      'name':                   product.name,
      'description':            product.description,
      'url':                    product.get_absolute_url(),

      'category':               product.category.name,
      'keywords':               product.category.keywords,
      'parent_category':        product.parent_category.name,
      'parent_keywords':        product.parent_category.keywords,

      'price':                  product.display_price,
      'shipping_price':         product.display_shipping_price,

      'ratings':                product.ratings,
      'avg_rating':             product.rating,

      'width':                  product.width,
      'height':                 product.height,
      'length':                 product.length,
      'weight':                 product.weight,

      'humanized_metric_dimensions':  product.metric_dimensions,
      'humanized_english_dimensions': product.english_dimensions,

      'seller_id':              product.seller.id,
      'seller_name':            product.seller.name,
      'seller_bio':             product.seller.bio,
      'seller_city':            product.seller.city,
      'seller_country':         product.seller.country.name,
      'seller_coordinates':     product.seller.coordinates,
      'seller_image':           product.seller.image.original,
      'seller_url':             product.seller.get_absolute_url(),
    }

    colors = []
    for color in product.colors.all():
      colors.append({
        'name':       color.name,
        'hex_value':  color.hex_value,
      })
    product_data['colors'] = colors

    photos = []
    for photo in product.photos.all():
      photos.append({
        'rank':       photo.rank,
        'original':   photo.original,
        'thumbnail':  photo.thumb_size,
        'pinkynail':  photo.pinky_size,
      })
    product_data['photos'] = photos

    artisans = []
    for artisan in product.assets.filter(ilk='artisan'):
      artisans.append({
        'name':           artisan.name,
        'title':          artisan.title,
        'description':    artisan.description,
        'image':          artisan.image.thumb_size,
        'headshot':       artisan.image.headshot,
      })
    product_data['artisans'] = artisans

    utilities = []
    for utility in list(chain(product.assets.filter(ilk='material'),
                              product.assets.filter(ilk='tool'))):
      utilities.append({
        'ilk':            utility.ilk,
        'name':           utility.name,
        'description':    utility.description,
        'image':          utility.image.thumb_size,
        'peephole':       utility.image.peephole,
      })
    product_data['utilities'] = utilities

    product_amalgam_bomb.append(product_data)

  response = {'products': product_amalgam_bomb}

  if request:
    return HttpResponse(json.dumps(response), mimetype='application/json')
  else:
    return response
