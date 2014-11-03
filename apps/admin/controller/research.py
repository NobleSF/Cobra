from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from apps.admin.utils.decorator import access_required
from django.contrib import messages
from datetime import datetime, timedelta
from apps.admin.models.account import Account
from apps.seller.models.product import Product

@access_required('admin')
def home(request):
  return render(request, 'research.html', {})

@access_required('admin')
def googleImageSearch(request):
  try:
    product_id = request.GET['product_id']
    product = Product.objects.get(id=product_id)

    keywords = [product.name.replace(" ","+")] #multi-word names have spaces
    if "other" not in product.category.name and not product.category.is_parent_category:
      keywords.append(product.category.name)

    optional_keywords = [ "Morocco", "Moroccan", "artisan",]
    optional_keywords += product.materials.values_list('name', flat=True)
    optional_keywords += product.colors.values_list('name', flat=True)
    optional_keywords += [product.category.keywords.replace(", ","+")]

    if not product.category.is_parent_category:
      optional_keywords += product.parent_category.name

    url = "https://www.google.com/search"
    url += "?as_q=" + "+".join(keywords)
    url += "&as_oq=" + "+".join(optional_keywords)
    url += "&tbm=isch" #image search
    url += "&tbs=isz:l,itp:photo" #large photos
    url += "&safe=active" #safe search

    return HttpResponseRedirect(url)

  except Exception as e:
    #print str(e)
    return redirect('admin:research')

@access_required('admin')
def etsySearch(request):
  pass
