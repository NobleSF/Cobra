from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from admin.controller import decorator

@access_required('seller')
def home(request, context={}):
  return render(request, 'seller/home.html')

@access_required('seller')
def edit(request):
  from seller.models import Seller
  from seller.controller.forms import SellerEditForm

  if request.method == 'POST':
    form = SellerEditForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      try: # it must be a post to work
        seller = Seller.objects.get(pk=request.session['seller_pk'])
        seller.update(data)
        seller.save()
        return HttpResponseRedirect('/seller/home/')

      except Exception as e:
        context = {'exception': e}

  else:
    form = SellerEditForm()
    form.fields['country'].widget.attrs['disabled'] = True
    form.fields['currency'].widget.attrs['disabled'] = True

  context = {'form': form}
  return render(request, 'seller/account/edit.html', context)

@access_required('seller')
def asset(request): # use api.jquery.com/jQuery.post/
  from seller.models import Asset
  from admin.models import Category
  from seller.controller.forms import SellerAssetForm
  try: # it must be a post to work
    form = SellerAssetForm(request.POST)
    form['seller'] = request.session['seller_pk']
    if form.is_valid():
      asset = Asset.objects.get_or_create(**form.cleaned_data)

      """ #I think modelForm will take care of this for us.
      if ilk == "product" and 'category' in request.POST:
        category_string = request.POST['category']
        #category string is a string of space separated category names
        category_object_list = []
        for category_name in category_string.split():
          #split() created a list of strings, one for each category name
          category_object = Category.object.get(name=category_name)
          category_object_list.append(category_object)

        asset.category.add(*category_object_list)
      """
      asset.save()
      context = {'sucess': True}
    else:
      context = {'problem': "invalid form data"}

  except Exception as e:
    context = {'exception': e}

  return HttpResponse(context) #ajax response
