from django.http import HttpResponse, Http404, HttpResponseRedirect
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

  return render(request, 'inventory/home.html', context)

@access_required('seller')
def create(request):
  from seller.models import Seller, Product
  try:
    product = Product(seller_id = request.session['seller_id'])
    product.save()
    #return HttpResponseRedirect('inventory/product/'+product.id+'/edit/')
    return redirect('seller:inventory edit', id=product.id)

  except Exception as e:
    context = {'exception': e}
    #return seller.home(request, context)
    return redirect('seller:home')

@access_required('seller')
def edit(request, product_id):
  from seller.models import Product, Asset, Photo
  from seller.controller.forms import ProductEditForm, PhotoForm

  if request.method == 'POST':
    try:
      product_form = ProductEditForm(request.POST)
    except Exception as e:
      context = {'except': e}

  else:
    product_form = ProductEditForm()

  photos = Photo.objects.all().filter(product_id=product_id)

  context = {
    'product_form': product_form,
    'photos':       photos,
    'photo_form':   PhotoForm()
  }
  return render(request, 'inventory/edit.html', context)

@access_required('seller') #it's the 'r' in crud, but is it even needed?
def detail(request, id):
  return render(request, 'inventory/detail.html')

@access_required('seller')
def delete(request, id):
  #archive product and return to product home
  return HttpResponseRedirect('seller/inventory')

def checkInventory():
  #delete empty products
  #for all products in seller
    #if product meets requirements for posting live
      #product.is_active = True
    #else
      #product.is_active = False
  return True
