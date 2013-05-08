from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.utils import simplejson
from apps.admin.controller.decorator import access_required
from django.views.decorators.csrf import csrf_exempt

@access_required('seller')
def home(request):
  from apps.seller.models import Seller, Product
  try:
    seller = Seller.objects.get(id=request.session['seller_id'])
    products = seller.product_set.all()
    context = {'products': products}
  except Exception as e:
    context = {'exception': e}

  return render(request, 'inventory/home.html', context)

@access_required('seller')
def create(request):
  from apps.seller.models import Seller, Product
  try:
    product = Product(seller_id = request.session['seller_id'])
    product.save()
    #return HttpResponseRedirect('inventory/product/'+product.id+'/edit/')
    return redirect( str(product.id) + '/edit')

  except Exception as e:
    context = {'exception': e}
    #return seller.home(request, context)
    return redirect('seller:home')

@access_required('seller')
def edit(request, product_id):
  from apps.seller.models import Product, Asset, Photo, ShippingOption
  from apps.admin.models import Color
  from apps.seller.controller.forms import ProductEditForm, PhotoForm
  product = Product.objects.get(id=product_id)

  if request.method == 'POST':
    try:
      product_form = ProductEditForm(request.POST)
      if product_form.is_valid():
        product_data    = product_form.cleaned_data

        product.price   = product_data['price']
        product.length  = product_data['length']
        product.width   = product_data['width']
        product.height  = product_data['height']
        product.weight  = product_data['weight']

        asset_ids = product_data['assets'].split(" ");
        while '' in asset_ids:
          asset_ids.remove('')
        product.assets.clear()
        for asset_id in asset_ids:
          product.assets.add(Asset.objects.get(id=asset_id))

        shipping_option_ids = product_data['shipping_options'].split(" ");
        while '' in shipping_option_ids:
          shipping_option_ids.remove('')
        product.shipping_options.clear()
        for shipping_option_id in shipping_option_ids:
          product.shipping_options.add(ShippingOption.objects.get(id=shipping_option_id))

        colors_ids = product_data['colors'].split(" ");
        while '' in colors_ids:
          colors_ids.remove('')
          product.colors.clear()
        for colors_id in colors_ids:
          product.colors.add(Color.objects.get(id=colors_id))

        context = {'success': "product saved"}
        return redirect('seller:home')

      else:
        context = {'problem': "form did not validate"}

    except Exception as e:
      context = {'except': e}

  else:
    product_form = ProductEditForm()
    product_form.fields['price'].initial  = product.price
    product_form.fields['length'].initial = product.length
    product_form.fields['width'].initial  = product.width
    product_form.fields['height'].initial = product.height
    product_form.fields['weight'].initial = product.weight

    assets = product.assets.all()
    for asset in assets:
      product_form.fields['assets'].initial += str(asset.id)+" "

    colors = product.colors.all()
    for color in colors:
      product_form.fields['colors'].initial += str(color.id)+" "

    shipping_options = product.shipping_options.all()
    for shipping_option in shipping_options:
      product_form.fields['shipping_options'].initial += str(shipping_option.id)+" "

  product_form.fields['product_id'].initial = product.id
  photos = Photo.objects.filter(product=product).order_by('rank')
  # we want additional ranks going up to nine photos maximum
  add_ranks_range = range(photos.count()+1, 10)

  photo_form = PhotoForm()
  photo_form.fields['tags'].initial = "product,seller"+str(request.session['seller_id'])
  photo_form.fields['timestamp'].initial = getUnixTimestamp()
  photo_form.fields['signature'].initial = getSignatureHash(photo_form)

  context = {
    'product':          product,
    'product_form':     product_form,
    'photos':           photos,
    'photo_form':       photo_form,
    'add_ranks_range':  add_ranks_range
  }
  return render(request, 'inventory/edit.html', context)

def getUnixTimestamp():
  from django.utils.dateformat import format
  from datetime import datetime
  return format(datetime.now(), u'U')

def getSignatureHash(photo_form):
  from settings.settings import CLOUDINARY
  import hashlib
  cloudinary_string  = 'format=' + photo_form.fields['format'].initial
  cloudinary_string += '&tags=' + photo_form.fields['tags'].initial
  cloudinary_string += '&timestamp=' + photo_form.fields['timestamp'].initial
  cloudinary_string += '&transformation=' + photo_form.fields['transformation'].initial
  cloudinary_string += CLOUDINARY['api_secret']

  h = hashlib.new('sha1')
  h.update(cloudinary_string)
  return h.hexdigest()

@access_required('seller') #it's the 'r' in crud, but is it even needed?
def detail(request, id):
  return render(request, 'inventory/detail.html')

@access_required('seller')
def delete(request, id):
  #archive product and return to product home
  return HttpResponseRedirect('seller/inventory')

def checkInventory():
  #delete empty products
  #for all products in seller
    #if product meets requirements for posting live
      #product.is_active = True
    #else
      #product.is_active = False
  return True

@access_required('seller')
@csrf_exempt
def saveProduct(request): #ajax requests only, not asset-aware
  from apps.seller.models import Product, Asset, ShippingOption
  from apps.admin.models import Color
  context = {}

  if request.method == 'GET': # it must be an ajax GET to work
    try:
      product_id = request.GET['product_id']
      product = Product.objects.get(id=product_id)
      attribute = request.GET['attribute']
      if 'status' in request.GET:
        status = request.GET['status']
      else:
        status = None

      if attribute == "asset":
        asset_id = request.GET['asset_id']
        asset = Asset.objects.get(id=asset_id)
        if status == "active":
          product.assets.add(asset)
          context['asset'] = "added asset " + str(asset.id)
        else:
          product.assets.remove(asset)
          context['asset'] = "removed asset " + str(asset.id)

      elif attribute == "shipping option":
        shipping_option_id = request.GET['shipping_option_id']
        shipping_option = ShippingOption.objects.get(id=shipping_option_id)
        if status == "active":
          product.shipping_options.add(shipping_option)
          context['shipping_option'] = "added shipping option "+str(shipping_option.id)
        else:
          product.shipping_options.remove(shipping_option)
          context['shipping_option'] = "removed shipping option "+str(shipping_option.id)

      elif attribute == "color":
        color_id = request.GET['color_id']
        color = Color.objects.get(id=color_id)
        if status == "active":
          product.colors.add(color)
          context['color'] = "added color " + str(color.id)
        else:
          product.colors.remove(color)
          context['color'] = "removed color " + str(color.id)

      elif attribute == "photo":
        photo_id = request.GET['photo_id']
        if not photo_id:
          photo_id = None
        rank = request.GET['rank']
        url = request.GET['value']
        photo = customSavePhoto(url, product_id, rank, photo_id)
        context['photo_id'] = photo.id
        context['photo'] = "saved photo at rank " + rank

      elif attribute == "price":
        product.price   = request.GET['value']
        context['price'] = "saved price: " + request.GET['value']
      elif attribute == "length":
        product.length  = request.GET['value']
        context['length'] = "saved length: " + request.GET['value']
      elif attribute == "width":
        product.width   = request.GET['value']
        context['width'] = "saved width: " + request.GET['value']
      elif attribute == "height":
        product.height  = request.GET['value']
        context['height'] = "saved height: " + request.GET['value']
      elif attribute == "weight":
        product.weight  = request.GET['value']
        context['weight'] = "saved weight: " + request.GET['value']

      product.save()
      context['success'] = attribute + " attribute saved"

    except Exception as e:
      context = {'exception': e}

  else:
    context['problem'] = "not GET"

  response = context
  return HttpResponse(simplejson.dumps(response), mimetype='application/json')
  #return HttpResponse(context['exception'])

def customSavePhoto(url, product_id, rank, photo_id=None):
  from apps.seller.models import Photo
  if photo_id:
    photo_object = Photo.objects.get(id=photo_id)
  else:
    photo_object = Photo(product_id=product_id, rank=rank, original=url)

  photo_object.thumb = url.replace("upload", "upload/t_thumb")
  photo_object.pinky = url.replace("upload", "upload/t_pinky")
  photo_object.save()
  return photo_object
