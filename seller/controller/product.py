from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from admin.controller.decorator import access_required

@access_required('seller')
def home(request):
  from seller.models import Seller, Product
  try:
    seller = Seller.objects.get(pk=request.session['seller_pk'])
    product = seller.product_set.all()
    context = {'success': "got your products"}
    context['product'] = product

  except Exception as e:
    context = {'exception': e}

  return render(request, 'product/home.html', context)

@access_required('seller')
def create(request):
  from seller.models import Seller, Product
  try:
    product = Product(seller = request.session['seller_pk'])
    product.save()
    return HttpResponseRedirect('product/'+product.pk+'/edit/')

  except Exception as e:
    context = {'exception': e}
    from seller.controller import seller
    return seller.home(request, context)

@access_required('seller')
def edit(request, id):
  from seller.models import Product, Asset
  from seller.controller.forms import ProductEditForm

  #assets = Asset.objects.all().filter(seller_id = request.session['seller_id'])

  if request.method == 'POST':
    product_form = ProductEditForm(request.POST)









  else:
    product_form = ProductEditForm()

  context = {
    'product_form': product_form
    #'assets': assets
  }
  return render(request, 'product/edit.html', context)

@access_required('seller')
def detail(request, id):
  return render(request, 'product/detail.html')

@access_required('seller')
def delete(request, id):
  #archive product and return to product home
  return render(request, 'product/home.html')
