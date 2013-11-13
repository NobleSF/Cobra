from django.http import HttpResponse
from django.utils import simplejson, timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.admin.utils.decorator import access_required
from apps.admin.utils.exception_handling import ExceptionHandler
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
<<<<<<< HEAD
from settings.people import Tom
from apps.communication.controller.email_class import Email
from apps.seller.models import Seller
=======
>>>>>>> origin/master

@access_required('seller')
def home(request):
  try:
    seller = Seller.objects.get(id=request.session['seller_id'])
    context = {'seller': seller}
  except Exception as e:
    ExceptionHandler(e, "in management.home")
    context = {'exception': e}

  return render(request, 'management/home.html', context)

@access_required('seller')
def products(request):
  try:
    seller = Seller.objects.get(id=request.session['seller_id'])
    products = (seller.product_set.filter(active_at__lte=timezone.now(),
                                          deactive_at=None,
                                          sold_at=None)
                                  .filter(
                                          Q(approved_at__lte=timezone.now()) |
                                          Q(in_holding=True)
                                  ))


    context = {'seller': seller, 'products': products}
  except Exception as e:
    ExceptionHandler(e, "in management.products")
    context = {'exception': e}

  return render(request, 'management/products.html', context)

@access_required('seller')
def orders(request):
  try:
    seller = Seller.objects.get(id=request.session['seller_id'])
    sold_products = seller.product_set.filter(sold_at__lte=timezone.now())
    for product in sold_products:
      product.order = product.order_set.all()[0]
    context = {'seller': seller, 'products': sold_products}

  except Exception as e:
    ExceptionHandler(e, "in management.products")
    context = {'exception': e}

  return render(request, 'management/orders.html', context)

@access_required('admin')
def etsy(request):
  from apps.etsy.controller.oauth import EtsyOAuthClient as OAuth
  from apps.etsy.controller.shop_class import Shop

  seller = Seller.objects.get(id=request.session['seller_id'])
  context = {'seller': seller}

  if request.method == "POST":
    if 'shop_name' in request.POST:
      etsy_shop_name = request.POST['shop_name']
      shop = Shop(seller, etsy_shop_name.strip())
    else:
      shop = Shop(seller)

    auth_code = request.POST.get('auth_code')
    #clean user input
    auth_code = auth_code.strip() if isinstance(auth_code, basestring) else None

    if auth_code and 'auth_token' in request.session:
      #verify and get authenticated tokens
      auth = OAuth(request.session['auth_token'])
      auth.set_oauth_verifier(auth_code)
      shop.shop.auth_token = auth.token.key
      shop.shop.auth_token_secret = auth.token.secret
      shop.shop.save()
      del request.session['auth_token']

  try:
    shop = Shop(seller)
    context['etsy_shop'] = shop.shop
    context['anou_data'] = shop.getAnouShopData()
    context['etsy_data'] = shop.getEtsyShopData()

    if not shop.shop.is_authorized:
      auth = OAuth()
      context['signin_url'] = auth.get_signin_url()
      print "signin url: " + context['signin_url']
      request.session['auth_token'] = auth.token

  except Exception as e:
    print str(e)

  return render(request, 'management/etsy.html', context)

@access_required('admin')
def updateEtsyShop(request):
  pass

@access_required('admin')
def ebay(request):
  return render(request, 'management/ebay.html', context)
