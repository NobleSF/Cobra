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

  AssetFormSet = formset_factory(AssetForm, can_delete=True, extra=30)

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

    asset_formset = AssetFormSet()

  context = {
              'seller_form': seller_form,
              'asset_formset': asset_formset,
              'asset_ilks': ['artisan','product','tool','material']
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
