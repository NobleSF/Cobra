from datetime import datetime
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from apps.seller.models.product import Product

def home(request, product_id, slug=None):
  product = get_object_or_404(Product, id=product_id)

  #permanent redirect when slug not included
  if product.slug and slug != product.slug:
    return redirect(product, permanent=True) #uses get_absolute_url

  return render(request, 'product.html', {'product': product})

def product_data(request):
  from django.utils import timezone
  product_amalgam_bomb = []

  products = Product.objects.filter(active_at__lte=timezone.now())

  if request.GET.get('product_id', None):
    products = products.filter(id=request.GET.get('product_id'))

  if request.GET.get('updated_since', None):
    timestamp = datetime.utcfromtimestamp(int(request.GET.get('updated_since')))
    products = products.filter(updated_at__gte=timestamp)
    #print "timestamp: " + str(timestamp)

  try:
    page = int(request.GET['page'])
    (start, end) = ((page-1)*10, (page * 10))
  except Exception as e:
    (start, end) = (0, 10)

  #print "product count: " + str(products.count())

  for product in products[start:end]:

    product_data = {
      'id':                     product.id,
      'name':                   product.name,
      'description':            product.description,
      'url':                    product.get_absolute_url(),

      'category':               product.category.name if product.category else "",
      'keywords':               product.category.keywords if product.category else "",
      'parent_category':        product.parent_category.name if product.parent_category else "",
      'parent_keywords':        product.parent_category.keywords if product.parent_category else "",

      'status':                 "unavailable" if (product.is_sold or not product.is_approved) else "available",
      'quantity':               1,
      'price':                  product.display_price*100,
      'shipping_price':         product.display_shipping_price*100,

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
      'seller_country':         product.seller.country.name if product.seller.country else "",
      'seller_coordinates':     product.seller.coordinates,
      'seller_image':           product.seller.image.original if product.seller.image else "",
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
        'image':          artisan.image.thumb_size if artisan.image else None,
        'headshot':       artisan.image.headshot if artisan.image else None,
      })
    product_data['artisans'] = artisans

    utilities = []
    for utility in product.utilities:
      utilities.append({
        'ilk':            utility.ilk,
        'name':           utility.name,
        'description':    utility.description,
        'image':          utility.image.thumb_size if utility.image else None,
        'peephole':       utility.image.peephole if utility.image else None,
      })
    product_data['utilities'] = utilities

    product_amalgam_bomb.append(product_data)

  response = {'products': product_amalgam_bomb}

  if request:
    return HttpResponse(json.dumps(response), content_type='application/json')
  else:
    return response
