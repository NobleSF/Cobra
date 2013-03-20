from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from admin.controller.decorator import access_required

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
  from seller.controller.forms import *
  from django.forms.formsets import formset_factory

  AssetProductFormSet   = formset_factory(AssetProductForm, extra=20,
                                          can_order=True, can_delete=True)
  AssetArtisanFormSet   = formset_factory(AssetForm, extra=20,
                                          can_order=True, can_delete=True)
  AssetToolFormSet      = formset_factory(AssetForm, extra=20,
                                          can_order=True, can_delete=True)
  AssetMaterialFormSet  = formset_factory(AssetForm, extra=20,
                                          can_order=True, can_delete=True)
  #use order fields as the rank number


  if request.method == 'POST':
    seller_form       = SellerEditForm(       request.POST)
    product_formset   = AssetProductFormSet(  request.POST, request.FILES, prefix='product')
    artisan_formset   = AssetArtisanFormSet(  request.POST, request.FILES, prefix='artisan')
    tool_formset      = AssetToolFormSet(     request.POST, request.FILES, prefix='tool')
    material_formset  = AssetMaterialFormSet( request.POST, request.FILES, prefix='material')

    try: # it must be a post to work
      if seller_form.is_valid():
        seller_data = seller_form.cleaned_data
        seller = Seller.objects.get(id=request.session['seller_id'])
        seller.update(data)
        seller.save()

      if product_formset.has_changed() and product_formset.is_valid():
        product_data = product_formset.cleaned_data
        product_asset = Asset.objects.get_or_create(
          id    = request.session['seller_pk'],
          ilk   = 'product',
          rank  = product_data['ORDER']
        )
        product_asset.update(data)
        product_asset.save()
      else:
        context = {'problem': "product asset data invalid"}

      #repeated for each asset ilk

        return HttpResponseRedirect('account/home/')

    except Exception as e:
      context = {'exception': e}

  else: #not POST
    seller_form       = SellerEditForm()
    if 'admin_id' not in request.session:
      seller_form.fields['country'].widget.attrs['disabled'] = True
      seller_form.fields['currency'].widget.attrs['disabled'] = True

    product_formset   = AssetProductFormSet(  prefix='product',
                                              initial=[{'ilk': u'product',}])
    artisan_formset   = AssetArtisanFormSet(  prefix='artisan',
                                              initial=[{'ilk': u'artisan',}])
    tool_formset      = AssetToolFormSet(     prefix='tool',
                                              initial=[{'ilk': u'tool',}])
    material_formset  = AssetMaterialFormSet( prefix='material',
                                              initial=[{'ilk': u'material',}])

  context = {
              'seller_form':      seller_form,
              'product_formset':  product_formset,
              'artisan_formset':  artisan_formset,
              'tool_formset':     tool_formset,
              'material_formset': material_formset,
            }
  return render(request, 'account/edit.html', context)

@access_required('seller')
def asset(request): # use api.jquery.com/jQuery.post/
  from seller.models import Asset
  from admin.models import Category
  from seller.controller.forms import AssetProductForm
  from django.forms.formsets import formset_factory

  try: # it must be a post to work
    AssetProductFormset = formset_factory(AssetProductForm)
    formset = AssetProductForm(request.POST, request.FILES)
    if formset.is_valid():
      #asset = Asset.objects.get_or_create(**form.cleaned_data)
      #if ilk...
      #asset.save()
      context = {'sucess': True}
    else:
      context = {'problem': "invalid form data"}

  except Exception as e:
    context = {'exception': e}

  return HttpResponse(context) #ajax response
