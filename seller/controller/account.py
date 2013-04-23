from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render, redirect
from admin.controller.decorator import access_required
from django.views.decorators.csrf import csrf_exempt

@access_required('seller')
def home(request, context={}):
  from seller.controller.inventory import checkInventory
  everything_checks_out = checkInventory()
  return render(request, 'account/home.html')

def create(account_id):
  try:
    from seller.models import Seller
    account = Seller(account_id=account_id)
    account.save()
    return True
  except Exception as e:
    context = {'exception': e}
    return False

@access_required('seller')
def edit(request):
  from seller.models import Seller, Asset
  from seller.controller.forms import AssetForm, ImageForm, SellerEditForm
  seller = Seller.objects.get(id=request.session['seller_id'])

  try:
    assets = Asset.objects.filter(seller_id=seller.id)
  except:
    assets = []

  image_form = ImageForm()
  image_form.fields['tags'].initial = "asset,seller"+str(request.session['seller_id'])
  image_form.fields['signature'].initial = getSignatureHash(image_form)

  context = {
              'assets': assets,
              'asset_form': AssetForm(),
              'image_form': image_form,
              'asset_ilks': ['artisan','product','tool','material']
            }

  if request.method == 'POST':
    seller_form = SellerEditForm(request.POST)
    try: # it must be a post to work
      if seller_form.is_valid():
        seller_data = seller_form.cleaned_data
        seller.name     = seller_data['name']
        seller.email    = seller_data['email']
        seller.phone    = seller_data['phone']
        seller.bio      = seller_data['bio']
        seller.country  = seller_data['country']
        seller.currency = seller_data['currency']
        seller.save()
        context = {'success': "Seller info saved"}
        return redirect('seller:home')

    except Exception as e:
      context['exception'] = e

  else: #not POST
    seller_form = SellerEditForm()
    seller_form.fields['name'].initial      = seller.name
    seller_form.fields['email'].initial     = seller.email
    seller_form.fields['phone'].initial     = seller.phone
    seller_form.fields['bio'].initial       = seller.bio
    seller_form.fields['country'].initial   = seller.country
    seller_form.fields['currency'].initial  = seller.currency
    if 'admin_id' not in request.session:
      seller_form.fields['country'].widget.attrs['disabled'] = True
      seller_form.fields['currency'].widget.attrs['disabled'] = True

  context['seller_form'] = seller_form

  return render(request, 'account/edit.html', context)

def getSignatureHash(image_form):
  from anou.settings import CLOUDINARY
  import hashlib

  cloudinary_string  = 'format=' + image_form.fields['format'].initial
  cloudinary_string += '&tags=' + image_form.fields['tags'].initial
  cloudinary_string += '&timestamp=' + image_form.fields['timestamp'].initial
  cloudinary_string += '&transformation=' + image_form.fields['transformation'].initial
  cloudinary_string += CLOUDINARY['api_secret']

  h = hashlib.new('sha1')
  h.update(cloudinary_string)
  return h.hexdigest()

@access_required('seller')
@csrf_exempt
def saveAsset(request): #ajax requests only, create or update asset
  from seller.models import Asset, Image
  from admin.models import Category
  from seller.controller.forms import AssetForm

  if request.method == 'GET': # it must be an ajax post to work
    try:
      asset = Asset(seller_id=request.session['seller_id'])
      if 'asset_id' in request.GET and request.GET['asset_id'] != "none":
        asset = Asset.objects.get(id=request.GET['asset_id'])

      asset.ilk = request.GET['ilk']#from data-ilk included in every request

      element = request.GET['name']
      value   = request.GET['value']
      if element == 'image_url':
        asset.image = customSaveImage(value)
      elif element == 'name':
        asset.name = value
      elif element == 'description':
        asset.description = value
      elif element == 'category':
        asset.category = value

      asset.save()
      context = {'asset_id':asset.id, 'get':request.GET}

      if 'DELETE' in request.GET:
        #asset.delete()
        #context = {'asset_id':"deleted"}
        pass #what do we do with products using this asset?

    except Exception as e:
      context = {'exception':e}
  else:
    context = {'problem':"not GET"}

  response = context
  return HttpResponse(simplejson.dumps(response), mimetype='application/json')

def customSaveImage(url):
  from seller.models import Image
  image_object = Image(original=url)
  image_object.thumb = url.replace("upload", "upload/t_thumb")
  image_object.pinky = url.replace("upload", "upload/t_pinky")
  image_object.save()
  return image_object

@access_required('seller')
@csrf_exempt
def saveImage(request): #ajax requests only, not asset-aware
  from seller.models import Image, Asset, Seller
  from seller.controller.forms import ImageForm
  from anou.settings import DEBUG, AWS_STATIC_URL
  from datetime import datetime
  from django.core.files.uploadedfile import SimpleUploadedFile
  from seller.controller.image_manipulation import makeThumbnails

  if request.method == 'POST':
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():
      try:
        #change filename(key) to seller_#_asset-ilk_date_orig-filename
        key = 'seller_' + "%04d" % request.session['seller_id']#4 digit seller id
        key += '_' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        key += '.jpg'

        image_model_object = form.save()
        original_url = AWS_STATIC_URL + str(image_model_object.original)

        (original_image, thumb_image, pinky_image) = makeThumbnails(original_url)

        image_model_object.original = SimpleUploadedFile(
                                    key,
                                    original_image,
                                    content_type='image/jpeg')

        image_model_object.thumb = SimpleUploadedFile(
                                    key,
                                    thumb_image,
                                    content_type='image/jpeg')

        image_model_object.pinky = SimpleUploadedFile(
                                    key,
                                    pinky_image,
                                    content_type='image/jpeg')

        image_model_object.save()

        context = { 'image_id':str(image_model_object.id),
                    'thumb_url':AWS_STATIC_URL+str(image_model_object.thumb)}

      except Exception as e:
        context = {'exception':e}
    else:
      context = {'problem':"couldn't validate"}
  else:
    context = {'problem':"not POST"}

  response = context
  return HttpResponse(simplejson.dumps(response), mimetype='application/json')
