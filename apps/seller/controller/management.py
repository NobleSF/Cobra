from django.http import HttpResponse
from django.utils import simplejson, timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.admin.controller.decorator import access_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from settings.people import Tom
from apps.communication.controller.email_class import Email

@access_required('seller')
def home(request):
  from apps.seller.models import Seller

  try:
    seller = Seller.objects.get(id=request.session['seller_id'])
    context = {'seller': seller}
  except Exception as e:
    Email(message="error on seller home: "+str(e)).sendTo(Tom.email)
    context = {'exception': e}

  return render(request, 'management/home.html', context)

@access_required('seller')
def products(request):
  from apps.seller.models import Seller

  try:
    seller = Seller.objects.get(id=request.session['seller_id'])
    products = (seller.product_set.filter(active_at__lte=timezone.now(),
                                          deactive_at=None,
                                          sold_at=None)
                                  .filter(
                                    Q(approved_at__lte=timezone.now()) |
                                    Q(in_holding=True)
                                  ))


    context = {'seller': seller, 'products': products}
  except Exception as e:
    Email(message="error on seller products page: "+str(e)).sendTo(Tom.email)
    context = {'exception': e}

  return render(request, 'management/products.html', context)

@access_required('seller')
def orders(request):
  from apps.seller.models import Seller

  try:
    seller = Seller.objects.get(id=request.session['seller_id'])
    sold_products = seller.product_set.filter(sold_at__lte=timezone.now())
    for product in sold_products:
      product.order = product.order_set.all()[0]
    context = {'seller': seller, 'products': sold_products}

  except Exception as e:
    Email(message="error on seller orders page: "+str(e)).sendTo(Tom.email)
    context = {'exception': e}

  return render(request, 'management/orders.html', context)

@access_required('seller')
@csrf_exempt
def imageFormData(request):
  from settings.settings import CLOUDINARY
  if request.method == "POST":
    seller_id   = request.session['seller_id']
    ilk         = request.POST['ilk']
    rank        = request.POST['rank']
    timestamp   = getUnixTimestamp()

    #uniquely name every image e.g. "seller23_ilkartisan_rank1_time1380924180"
    image_id  = "seller"+str(seller_id)
    image_id += "_ilk"+str(ilk)
    image_id += "_rank"+str(rank)
    image_id += "_time"+str(timestamp)
    #tag image with seller_id and asset_ilk
    tags = "seller"+str(seller_id)+",asset"+str(ilk)

    form_data = {
      'public_id':      image_id,
      'tags':           tags,
      'api_key':        CLOUDINARY['api_key'],
      'format':         CLOUDINARY['format'],
      'transformation': CLOUDINARY['transformation'],
      'timestamp':      timestamp,
    }
    form_data['signature'] = createSignature(form_data)
  return HttpResponse(simplejson.dumps(form_data), mimetype='application/json')

@access_required('admin or seller')
@csrf_exempt
def photoFormData(request):
  from settings.settings import CLOUDINARY
  if request.method == "POST":
    seller_id   = request.session['seller_id']
    product_id  = request.POST['product']
    rank        = request.POST['rank']
    timestamp   = getUnixTimestamp()

    #uniquely name every photo e.g. "seller23_product1024_rank1"
    photo_id  = "seller"+str(seller_id)
    photo_id += "_product"+str(product_id)
    photo_id += "_rank"+str(rank)
    photo_id += "_time"+str(timestamp)
    #tag photo with product_id and seller_id
    tags = "product"+str(product_id)+",seller"+str(seller_id)

    form_data = {
      'public_id':      photo_id,
      'tags':           tags,
      'api_key':        CLOUDINARY['api_key'],
      'format':         CLOUDINARY['format'],
      'transformation': CLOUDINARY['transformation'],
      'timestamp':      timestamp,
    }
    form_data['signature'] = createSignature(form_data)
  return HttpResponse(simplejson.dumps(form_data), mimetype='application/json')

def getUnixTimestamp():
  from django.utils.dateformat import format
  from django.utils import timezone
  return format(timezone.now(), u'U')

def createSignature(data):
  from settings.settings import CLOUDINARY
  import hashlib
  cloudinary_string  = 'format='          + data['format']
  cloudinary_string += '&public_id='      + data['public_id']
  cloudinary_string += '&tags='           + data['tags']
  cloudinary_string += '&timestamp='      + data['timestamp']
  cloudinary_string += '&transformation=' + data['transformation']
  cloudinary_string += CLOUDINARY['api_secret']

  h = hashlib.new('sha1')
  h.update(cloudinary_string)
  return h.hexdigest()
