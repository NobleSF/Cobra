from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from admin.controller import decorator

@decorator.requires_seller_or_admin
def home(request):
  return render(request, 'seller/home.html')

@decorator.requires_seller_or_admin
def edit(request):
  if request.method == 'POST':
    try: # it must be a post to work
      name      = request.POST['name']
      email     = request.POST['email']
      phone     = request.POST['phone']
      bio       = request.POST['bio']
      country   = request.POST['country']
      currency  = request.POST['currency']

      seller = Seller.objects.get(pk=request.session['seller_pk'])

    except Exception as e:
      context = {'exception': e}

  #collect all seller info and assets for template

  return render(request, 'seller/edit.html')

@decorator.requires_seller_or_admin
def asset(request): # use api.jquery.com/jQuery.post/
  try: # it must be a post to work
    ilk =          request.POST['asset_ilk']
    identifier =   request.POST['asset_identifier']
    name =         request.POST['asset_name']
    description =  request.POST['asset_description']

    from seller.models import Asset
    asset = Asset.objects.get_or_create(
      ilk = ilk,
      identifier = identifier
    )

    asset.name = name
    asset.description = description

    if ilk == "product" and 'category_list' in request.POST:
      for category in request.POST['category_list']:
        asset.category = attribute_list['category_array'][category]

    asset.save()
    context = {'sucess': "asset saved"}

  except Exception as e:
    context = {'exception': e}
  return render(request, 'seller/asset.html', context)
