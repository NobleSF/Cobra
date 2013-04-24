from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.shortcuts import render, redirect
from admin.controller.decorator import access_required
from django.views.decorators.csrf import csrf_exempt

@access_required('seller')
def home(request):
  from seller.models import Seller, Product
  try:
    seller = Seller.objects.get(pk=request.session['seller_pk'])
    product = seller.product_set.all()
    context = {'success': "got your products"}
    context['product'] = product

  except Exception as e:
    context = {'exception': e}

  return render(request, 'inventory/home.html', context)

@access_required('seller')
def create(request):
  from seller.models import Seller, Product
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
  from seller.models import Product, Asset, Photo
  from seller.controller.forms import ProductEditForm, PhotoForm
  product = Product.objects.get(id=product_id)

  if request.method == 'POST':
    try:
      product_form = ProductEditForm(request.POST)
    except Exception as e:
      context = {'except': e}

  else:
    product_form = ProductEditForm()

  product_form.fields['product_id'].initial = product.id
  photos = Photo.objects.all().filter(product_id=product_id).order_by('rank')
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
  from anou.settings import CLOUDINARY
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
  pass
