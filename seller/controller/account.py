from django.http import HttpResponse, Http404
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from admin.controller.decorator import access_required
from django.views.decorators.csrf import csrf_exempt

@access_required('seller')
def home(request, context={}):
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
  from seller.models import Seller
  from seller.controller.forms import AssetForm, ImageForm, SellerEditForm
  if request.method == 'POST':

    seller_form = SellerEditForm(request.POST)
    try: # it must be a post to work
      if seller_form.is_valid():
        seller_data = seller_form.cleaned_data
        seller = Seller.objects.get(id=request.session['seller_id'])
        seller.update(data)
        seller.save()
        return HttpResponseRedirect('account/home/')

    except Exception as e:
      context = {'exception': e}

  else: #not POST
    seller_form   = SellerEditForm()
    if 'admin_id' not in request.session:
      seller_form.fields['country'].widget.attrs['disabled'] = True
      seller_form.fields['currency'].widget.attrs['disabled'] = True

    asset_form = AssetForm()
    image_form = ImageForm()

  context = {
              'seller_form': seller_form,
              'asset_form': asset_form,
              'image_form': image_form,
              'asset_ilks': ['artisan','product','tool','material']
            }
  return render(request, 'account/edit.html', context)

@access_required('seller')
def saveAsset(request): # use api.jquery.com/jQuery.post/
  from seller.models import Asset
  from admin.models import Category
  from seller.controller.forms import AssetProductForm

  try: # it must be an ajax post to work
    form = AssetForm(request.POST, request.FILES)
    if formset.is_valid():
      #asset = Asset.objects.get_or_create(**form.cleaned_data)
      #use image url to lookup image and assign it
      #asset.save()
      context = {'sucess': True}
    else:
      context = {'problem': "invalid form data"}

  except Exception as e:
    context = {'exception': e}

  return HttpResponse(context) #ajax response

@access_required('seller')
@csrf_exempt
def saveImage(request): #ajax requests only, not asset-aware
  from seller.models import Image, Asset, Seller
  from seller.controller.forms import ImageForm
  from anou.settings import DEBUG, THUMBNAIL_ALIASES, AWS_STATIC_URL
  from datetime import datetime
  from django.core.files.uploadedfile import SimpleUploadedFile
  from seller.controller.image_manipulation import scaleImage

  if request.method == 'POST':
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():

      #change filename(key) to seller_#_asset-ilk_date_orig-filename
      key = 'seller_' + "%04d" % request.session['seller_id']#4 digit seller id
      key += '_' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
      key += '.jpg'

      original_dimensions = THUMBNAIL_ALIASES['original']['size']
      thumb_dimensions    = THUMBNAIL_ALIASES['thumb']['size']
      pinky_dimensions    = THUMBNAIL_ALIASES['pinky']['size']

      image_model_object = form.save()
      original_url = AWS_STATIC_URL + str(image_model_object.original)

      image_model_object.original = SimpleUploadedFile(
                                  key,
                                  scaleImage(original_url, original_dimensions),
                                  content_type='image/jpeg')

      image_model_object.thumb = SimpleUploadedFile(
                                  key,
                                  scaleImage(original_url, thumb_dimensions),
                                  content_type='image/jpeg')

      image_model_object.pinky = SimpleUploadedFile(
                                  key,
                                  scaleImage(original_url, pinky_dimensions),
                                  content_type='image/jpeg')

      image_model_object.save()

      context = {'thumb_url':AWS_STATIC_URL+str(image_model_object.pinky)}

    else:
      context = {'problem':"couldn't validate", }
  else:
    context = {'problem':"not POST"}

  #save all images to AWS

  response = context
  return HttpResponse(simplejson.dumps(response), mimetype='application/json')
