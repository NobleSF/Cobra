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
  photos = Photo.objects.all().filter(product_id=product_id).order_by(rank)

  context = {
    'product':        product,
    'product_form':   product_form,
    'photos':         photos,
    'photo_form':     PhotoForm(),
    'photo_ajax_url': ''
  }
  return render(request, 'inventory/edit.html', context)

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
def savePhoto(request): #ajax requests only, not asset-aware
  from seller.models import Photo, Product, Seller
  from seller.controller.forms import PhotoForm
  from anou.settings import DEBUG, AWS_STATIC_URL
  from datetime import datetime
  from django.core.files.uploadedfile import SimpleUploadedFile
  from seller.controller.image_manipulation import makeThumbnails

  if request.method == 'POST':
    form = PhotoForm(request.POST, request.FILES)
    if form.is_valid():
      try:
        #change filename(key) to seller_#_date.jpg
        key = 'seller_' + "%04d" % request.session['seller_id']#4 digit seller id
        key += '_' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        key += '.jpg'

        photo_model_object = form.save()
        original_url = AWS_STATIC_URL + str(photo_model_object.original)

        (original_photo, thumb_photo, pinky_photo) = makeThumbnails(original_url)

        photo_model_object.original = SimpleUploadedFile(
                                    key,
                                    original_photo,
                                    content_type='image/jpeg')

        photo_model_object.thumb = SimpleUploadedFile(
                                    key,
                                    thumb_photo,
                                    content_type='image/jpeg')

        photo_model_object.pinky = SimpleUploadedFile(
                                    key,
                                    pinky_photo,
                                    content_type='image/jpeg')

        photo_model_object.save()

        context = { 'photo_id':str(photo_model_object.id),
                    'thumb_url':AWS_STATIC_URL+str(photo_model_object.thumb)}

      except Exception as e:
        context = {'exception':e}
    else:
      context = {'problem':"couldn't validate"}
  else:
    context = {'problem':"not POST"}

  response = context
  return HttpResponse(simplejson.dumps(response), mimetype='application/json')
