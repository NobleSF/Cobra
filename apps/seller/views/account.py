from django.http import HttpResponse
import json
from django.shortcuts import render, redirect
from apps.admin.utils.decorator import access_required
from apps.admin.utils.exception_handling import ExceptionHandler
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError, transaction

def create(account):
  try:
    from apps.seller.models.seller import Seller
    seller_account = Seller(account_id=account.id)
    seller_account.save()
    return True
  except Exception as e:
    ExceptionHandler(e, "in account.create")
    return False

@access_required('seller')
def edit(request):
  from apps.seller.models.seller import Seller
  from apps.seller.views.forms import SellerEditForm
  from settings import CLOUDINARY

  seller = Seller.objects.get(id=request.session['seller_id'])
  try:
    context = {
                'seller':     seller,
                'assets':     seller.asset_set.order_by('id'),
                'asset_ilks': ['artisan','product','tool','material'],
                'CLOUDINARY': {'upload_url':   CLOUDINARY['upload_url'],
                               'download_url': CLOUDINARY['download_url']
                              }
              }

    if request.method == 'POST':
      POST = request.POST.copy()

      #fields only editable by admin, overwrite their values
      if 'admin_id' not in request.session:
        for fieldname in ['name',
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
          seller.account.email        = seller_data['email'] or None
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

          return redirect('seller:home')
        else:
          messages.warning(request, 'Invalid information entered')

      except IntegrityError:
        transaction.rollback()
        messages.warning(request, 'Another account is using this email or phone')

      except Exception as e:
        context['exception'] = e

    else: #not POST
      seller_form = SellerEditForm()
      seller_form.fields['email'].initial         = seller.email
      seller_form.fields['phone'].initial         = seller.phone

      seller_form.fields['name'].initial          = seller.name
      seller_form.fields['bio'].initial           = seller.bio
      seller_form.fields['bio_ol'].initial        = seller.bio_ol

      seller_form.fields['city'].initial          = seller.city
      seller_form.fields['country'].initial       = seller.country if seller.country else '1'
      seller_form.fields['coordinates'].initial   = seller.coordinates

      seller_form.fields['bank_name'].initial     = seller.bank_name
      seller_form.fields['bank_account'].initial  = seller.bank_account

      #disable fields only editable by admin
      if 'admin_id' not in request.session:
        for fieldname in ['name',]:
          seller_form.fields[fieldname].widget.attrs['disabled'] = True

    context['seller_form'] = seller_form

  except Exception as e:
    ExceptionHandler(e, "in account.edit")
    context = {'exception': str(e)}
    context['seller'] = seller

  return render(request, 'account/edit_seller.html', context)

@access_required('seller')
@csrf_exempt
def Asset(request): #ajax get requests only, create or update asset
  from apps.seller.models.asset import Asset
  from apps.admin.models.category import Category

  try:
    if request.method == 'POST':
      asset, is_new = Asset.objects.get_or_create(
                            seller_id = request.session['seller_id'],
                            ilk = request.POST['ilk'],
                            rank = request.POST['rank']
                          )

      element = request.POST.get('name')
      value   = request.POST.get('value', None)

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
        if value:
          asset.categories.add(Category.objects.get(id=value))
      asset.save()

      if element == 'delete' and value == 'delete':
        #todo: archive asset in reporting app
        asset.delete()

      response = {'asset_id':asset.id, 'element':element, 'value':value}
    else:
      response = {'problem': "not a POST request"}

  except Exception as e:
    #ExceptionHandler(e, "in account.saveAsset")
    response = {'exception': str(e)}
    return HttpResponse(json.dumps(response), status=400, content_type='application/json')

  else:
    return HttpResponse(json.dumps(response), content_type='application/json')
