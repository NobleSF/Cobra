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
  from apps.seller.controller.forms import AssetForm, SellerEditForm
  from settings.settings import CLOUDINARY

  seller = Seller.objects.get(id=request.session['seller_id'])
  try:
    context = {
                'seller':     seller,
                'assets':     seller.asset_set.order_by('id'),
                'asset_form': AssetForm(),
                'asset_ilks': ['artisan','product','tool','material'],
                'CLOUDINARY': {'upload_url':   CLOUDINARY['upload_url'],
                               'download_url': CLOUDINARY['download_url']
                              }
              }

    if request.method == 'POST':
      POST = request.POST.copy()

      #fields only editable by admin, overwrite their values
      if 'admin_id' not in request.session:
        for fieldname in ['name', 'username',
                          'bio', 'city', 'coordinates',
                          'bank_name', 'bank_account']:
          POST[fieldname] = eval("seller."+fieldname)

        for fieldname in ['country']:
          POST[fieldname] = eval("seller."+fieldname+".id")

      seller_form = SellerEditForm(POST)
      try: # it must be a post to work
        if seller_form.is_valid():
          seller_data = seller_form.cleaned_data

          seller.account.name         = seller_data['name']
          seller.account.username     = seller_data['username']
          seller.account.email        = seller_data['email']
          seller.account.phone        = seller_data['phone']
          seller.account.bank_name    = seller_data['bank_name']
          seller.account.bank_account = seller_data['bank_account']
          seller.account.save()

          seller.bio                  = seller_data['bio']
          seller.bio_ol               = seller_data['bio_ol']
          seller.country              = seller_data['country']
          seller.city                 = seller_data['city']
          seller.coordinates          = seller_data['coordinates']
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
      seller_form.fields['username'].initial      = seller.username
      seller_form.fields['email'].initial         = seller.email
      seller_form.fields['phone'].initial         = seller.phone

      seller_form.fields['name'].initial          = seller.name
      seller_form.fields['bio'].initial           = seller.bio
      seller_form.fields['bio_ol'].initial        = seller.bio_ol

      seller_form.fields['city'].initial          = seller.city
      seller_form.fields['country'].initial       = seller.country
      seller_form.fields['coordinates'].initial   = seller.coordinates

      seller_form.fields['bank_name'].initial     = seller.bank_name
      seller_form.fields['bank_account'].initial  = seller.bank_account

      #disable fields only editable by admin
      if 'admin_id' not in request.session:
        for fieldname in ['name', 'username']:
          seller_form.fields[fieldname].widget.attrs['disabled'] = True

    context['seller_form'] = seller_form

  except Exception as e:
    context = {'except':e}
    Email(message="error on Seller edit page: "+str(e)).sendTo(Tom.email)
    context['seller'] = seller

  return render(request, 'account/edit_seller.html', context)

@access_required('seller')
@csrf_exempt
def saveAsset(request): #ajax get requests only, create or update asset
  from apps.seller.models import Asset
  from apps.admin.models import Category

  try:
    asset, is_new = Asset.objects.get_or_create(
                        seller_id = request.session['seller_id'],
                        ilk = request.GET['ilk'],
                        rank = request.GET['rank']
                      )

    element = request.GET.get('name')
    value   = request.GET.get('value')

    if element == 'name':
      asset.name = value
    elif element == 'name_ol':
      asset.name_ol = value
    elif element == 'description':
      asset.description = value
    elif element == 'description_ol':
      asset.description_ol = value
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

  return HttpResponse(simplejson.dumps(response), mimetype='application/json')

@access_required('seller')
@csrf_exempt
def deleteAsset(request): #ajax requests only
  from apps.seller.models import Asset
  try:
    asset = Asset.objects.get(
              seller_id = request.session['seller_id'],
              ilk = request.GET['ilk'],
              rank = request.GET['rank']
            )
    asset.delete()
    response = {'deleted': "asset has been permanently deleted"}

  except Exception as e:
    response = {'exception': str(e)}
    Email(message="error in deleteAsset ajax: "+str(e)).sendTo(Tom.email)

  return HttpResponse(simplejson.dumps(response), mimetype='application/json')
