from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from admin.controller import decorator

@decorator.requires_seller_or_admin
def home(request):
  from seller.models import Seller, Product
  try:
    seller = Seller.objects.get(pk=request.session['seller_pk'])
    product = seller.product_set.all()
    context = {'success': "got your products"}
    context['product'] = product

  except Exception as e:
    context = {'exception': e}

  return render(request, 'seller/product/home.html', context)

@decorator.requires_seller_or_admin
def create(request):
  from seller.models import Seller, Product
  try:
    product = Product(seller = request.session['seller_pk'])
    product.save()
    return HttpResponseRedirect('seller/product/'+product.pk+'/edit/')

  except Exception as e:
    context = {'exception': e}
    from seller.controller import seller
    return seller.home(request, context)

@decorator.requires_seller_or_admin
def edit(request, id):
  from seller.models import Product
  """
  product = Product.objects.get(pk=id)

  # if form was submitted
  if request.method == 'POST':
    try:
      asset           = request.POST['asset']
      color           = request.POST['color']
      width           = request.POST['width']
      height          = request.POST['height']
      length          = request.POST['length']
      weight          = request.POST['weight']
      price           = request.POST['price']
      shipping_option = request.POST['shipping_option']
      #validate these

      #loop over assets

      #loop over colors

      #set values
      product.width           = width
      product.height          = height
      product.length          = length
      product.weight          = weight
      product.price           = price
      product.shipping_option = shipping_option

    except Exception as e:
      context = {'exception': e}

  else:
    context = {'success': 'go edit something'}

  """
  return render(request, 'seller/product/edit.html')#, context)

@decorator.requires_seller_or_admin
def detail(request, id):
  return render(request, 'seller/product/detail.html')

@decorator.requires_seller_or_admin
def delete(request, id):
  #archive product and return to product home
  return render(request, 'seller/product/home.html')
