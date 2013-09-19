from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render, redirect
from apps.admin.controller.decorator import access_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError, transaction
from settings.people import Tom
from apps.communication.controller.email_class import Email

def create(account):
  try:
    from apps.seller.models import Seller
    seller_account = Seller(account_id=account.id)
    seller_account.save()
    return True
  except Exception as e:
    context = {'exception': e}
    return e

@access_required('seller')
def edit(request):
  from apps.seller.models import Seller
  from apps.seller.controller.forms import AssetForm, ImageForm, SellerEditForm
  from settings.settings import CLOUDINARY

  seller = Seller.objects.get(id=request.session['seller_id'])
  try:
    image_form = ImageForm()
    image_form.fields['tags'].initial = "asset,seller"+str(request.session['seller_id'])
    image_form.fields['timestamp'].initial = getUnixTimestamp()
    image_form.fields['signature'].initial = getSignatureHash(image_form)

    context = {
                'seller':     seller,
                'assets':     seller.asset_set.all(),
                'asset_form': AssetForm(),
                'image_form': image_form,
                'asset_ilks': ['artisan','product','tool','material'],
                'CLOUDINARY': {'upload_url':   CLOUDINARY['upload_url'],
                               'download_url': CLOUDINARY['download_url']
                              }
              }

    if request.method == 'POST':
      POST = request.POST.copy()

      #fields only editable by admin
      if 'admin_id' not in request.session:
        for fieldname in ['name', 'city', 'coordinates']:
          POST[fieldname] = eval("seller."+fieldname)
        for fieldname in ['country', 'currency']:
          POST[fieldname] = eval("seller."+fieldname+".id")

      seller_form = SellerEditForm(POST)
      try: # it must be a post to work
        if seller_form.is_valid():
          seller_data = seller_form.cleaned_data

          seller.account.name   = seller_data['name']
          seller.account.email  = seller_data['email']
          seller.account.phone  = seller_data['phone']
          seller.account.save()

          seller.bio            = seller_data['bio']
          seller.city           = seller_data['city']
          seller.country        = seller_data['country']
          seller.coordinates    = seller_data['coordinates']
          seller.currency       = seller_data['currency']
          seller.save()

          return redirect('seller:management home')
        else:
          messages.warning(request, 'Invalid information entered')

      except IntegrityError:
        transaction.rollback()
        messages.warning(request, 'Another account is using this email or phone')

      except Exception as e:
        context['exception'] = e

    else: #not POST
      seller_form = SellerEditForm()
      seller_form.fields['name'].initial        = seller.name
      seller_form.fields['email'].initial       = seller.email
      seller_form.fields['phone'].initial       = seller.phone
      seller_form.fields['bio'].initial         = seller.bio
      try: seller_form.fields['image'].initial  = seller.image_id
      except: pass
      seller_form.fields['city'].initial        = seller.city
      seller_form.fields['country'].initial     = seller.country
      seller_form.fields['coordinates'].initial = seller.coordinates
      seller_form.fields['currency'].initial    = seller.currency

      #disable fields only editable by admin
      if 'admin_id' not in request.session:
        for fieldname in ['name', 'city', 'country', 'coordinates', 'currency']:
          seller_form.fields[fieldname].widget.attrs['disabled'] = True

    context['seller_form'] = seller_form

  except Exception as e:
    context = {'except':e}
    Email(message="error on Seller edit page: "+str(e)).sendTo(Tom.email)
    context['seller'] = seller

  return render(request, 'account/edit_seller.html', context)

def getUnixTimestamp():
  from django.utils.dateformat import format
  from django.utils import timezone
  return format(timezone.now(), u'U')

def getSignatureHash(image_form):
  from settings.settings import CLOUDINARY
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
def saveSeller(request): #ajax requests only, create or update asset
  from apps.seller.models import Seller

  if request.method == 'GET': # it must be an ajax post to work
    try:
      seller = Seller.objects.get(id=request.session['seller_id'])
      element = request.GET['name']
      value   = request.GET['value']

      if element == 'image_url':
        seller.image = customSaveImage(value)

      seller.save()
      response = {'success': element + " saved with value: " + value}

    except Exception as e:
      response = {'exception':e}
      Email(message="error in saveSeller: "+str(e)).sendTo(Tom.email)
  else:
    response = {'problem':"not GET"}

  return HttpResponse(simplejson.dumps(response), mimetype='application/json')

@access_required('seller')
@csrf_exempt
def saveAsset(request): #ajax requests only, create or update asset
  from apps.seller.models import Asset
  from apps.admin.models import Category

  if request.method == 'GET': # it must be an ajax get to work
    try:
      if (not request.GET.get('asset_id')) or request.GET.get('asset_id') == "none":
        #create new asset
        asset = Asset(seller_id=request.session.get('seller_id'))
      elif request.GET.get('asset_id') == "pending":
        raise Exception("asset_id is already pending")
      else:
        asset = Asset.objects.get(id=request.GET.get('asset_id'))

      asset.ilk = request.GET.get('ilk')#from data-ilk included in every request
      element = request.GET.get('name')
      value   = request.GET.get('value')

      if element == 'image_url':
        asset.image = customSaveImage(value)
      elif element == 'name':
        asset.name = value
      elif element == 'description':
        asset.description = value
      elif element == 'phone':
        asset.phone = value
      elif element == 'category':
        asset.categories.clear()
        asset.categories.add(Category.objects.get(id=value))

      asset.save()
      response = {'asset_id':asset.id, 'get':request.GET}

    except Exception as e:
      response = {'exception': str(e)}
      Email(message="error in saveAsset ajax: "+str(e)).sendTo(Tom.email)
  else:
    response = {'problem':"not GET"}

  return HttpResponse(simplejson.dumps(response), mimetype='application/json')

@access_required('seller')
@csrf_exempt
def deleteAsset(request): #ajax requests only
  from apps.seller.models import Asset
  try:
    asset = Asset.objects.get(id=request.GET['asset_id'])
    #todo: what do we do with products using this asset?
    asset.delete()
    response = {'deleted': "asset has been permanently deleted",
                'asset_id': request.GET['asset_id']
               }
  except Exception as e:
    response = {'exception': str(e), 'asset_id': 'None'}
    Email(message="error in deleteAsset ajax: "+str(e)).sendTo(Tom.email)

  return HttpResponse(simplejson.dumps(response), mimetype='application/json')

def customSaveImage(url):
  from apps.seller.models import Image
  try:
    image_object = Image(original=url)
    image_object.save()
    return image_object
  except: return None
