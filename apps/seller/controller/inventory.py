from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils import simplejson
from apps.admin.controller.decorator import access_required
from django.views.decorators.csrf import csrf_exempt
from apps.seller.models import Seller
from apps.seller.controller.product_class import Product
from settings.people import Tom
from apps.communication.controller.email_class import Email

def checkInventory(seller):
  #preferred method
  #inactive_products = seller.product_set.filter('is_active' = False)
  #if len(inactive_products) > 1:
  #  inactive_products[1:].delete()

  #hacked method: keep first inactive, else delete
  try:
    keep = 1
    for product in seller.product_set.all().order_by('id'):
      if product.was_never_active:
        if keep <= 0:
          product.delete()
        keep -= 1
  except:
    return False
  else:
    return True

@access_required('seller')
def create(request):
  seller = Seller.objects.get(id=request.session['seller_id'])
  checkInventory(seller)
  try:
    edit_this_product = None
    for product in seller.product_set.all().order_by('id'):
      if product.was_never_active and edit_this_product == None:
        edit_this_product = product

    if edit_this_product:
      request.product_id = edit_this_product.id

    #if no product id in request at this point, this will create a new one
    product_object = Product(request)
    return redirect("%d/edit" % product_object.product.id)

  except Exception as e:
    Email(message="error creating product: "+str(e)).sendTo(Tom.email)
    return redirect('seller:management home')

@access_required('admin or seller')
def edit(request, product_id):
  from apps.seller.controller.forms import ProductEditForm, PhotoForm
  from apps.seller.controller.management import signForm
  from settings.settings import CLOUDINARY

  try:
    request.product_id = product_id
    product = Product(request)

    product_form = ProductEditForm()
    product_form.fields['price'].initial  = product.get('price')
    product_form.fields['length'].initial = product.get('length')
    product_form.fields['width'].initial  = product.get('width')
    product_form.fields['height'].initial = product.get('height')
    product_form.fields['weight'].initial = product.get('weight')

    for asset in product.product.assets.all():
      product_form.fields['assets'].initial += str(asset.id)+" "

    for color in product.product.colors.all():
      product_form.fields['colors'].initial += str(color.id)+" "

    for shipping_option in product.product.shipping_options.all():
      product_form.fields['shipping_options'].initial += str(shipping_option.id)+" "

    product_form.fields['product_id'].initial = product.product.id

    product.product.photos = product.product.photo_set.order_by('rank')

    context = {
      'product':          product.product,
      'product_form':     product_form,
      'photo_form':       PhotoForm(),
      'CLOUDINARY':       {'upload_url':   CLOUDINARY['upload_url'],
                           'download_url': CLOUDINARY['download_url']
                          }
    }
    return render(request, 'inventory/edit.html', context)

  except Exception as e:
    Email(message="error loading product-edit: "+str(e)).sendTo(Tom.email)
    return redirect('seller:management home')

@access_required('seller') #it's the 'r' in crud, but is it even needed?
def detail(request, product_id):
  return render(request, 'inventory/detail.html')

@access_required('seller')
def remove(request, product_id): #archive product and return to management home
  try:
    request.product_id = product_id
    product = Product(request)
    if product.deactivate():
      if request.session.get('admin_id'):
        messages.success(request, "product %d removed." % product.product.id)
    else:
      if request.session.get('admin_id'):
        messages.error(request, "cannot not remove that product")
  except Exception as e:
    Email(message="error removing product: "+str(e)).sendTo(Tom.email)
    context = {'exception':e}

  return redirect('seller:management products')

@access_required('admin or seller')
@csrf_exempt
def saveProduct(request): #ajax requests only, not asset-aware
  response = {}

  if request.method == 'GET': # it must be an ajax GET to work
    try:
      request.product_id = request.GET['product_id']
      product = Product(request)

      if 'activate' in request.GET and request.GET['activate'] == "yes":
        product.activate();

      attribute = request.GET.get('attribute')
      status    = request.GET.get('status')
      if attribute and attribute != "active":
        product.unapprove()

      if attribute == "asset":
        if status == "active":
          response['asset'] = product.addAsset(request.GET['asset_id'])
        else:
          response['asset'] = product.removeAsset(request.GET['asset_id'])

      elif attribute == "shipping option":
        if status == "active":
          response['shipping_option'] = product.addShippingOption(request.GET['shipping_option_id'])
        else:
          response['shipping_option'] = product.removeShippingOption(request.GET['shipping_option_id'])

      elif attribute == "color":
        if status == "active":
          response['color'] = product.addColor(request.GET['color_id'])
        else:
          response['color'] = product.removeColor(request.GET['color_id'])

      elif attribute == "photo":
        try:
          photo_id = request.GET.get('photo_id')
          rank = request.GET.get('rank')
          url = request.GET.get('value')
        except: response['photo'] = "error saving photo"
        else:
          try:
            photo = product.addPhoto(url, rank, photo_id)
          except:
            response['photo'] = "error saving photo"
          else:
            response['photo_id'] = photo.id
            response['photo'] = "saved photo at rank %s with url %s" % (photo.rank, photo.original)

      elif attribute == "active":
        if status == "yes":
          response['active'] = product.activate()
        else:
          response['active'] = not product.deactivate()

      else:
        success_message = product.update(attribute, request.GET['value'])
        response['success'] = success_message

      cost_summary = {
        'summary_price': str(product.product.price) if product.product.price else "",
        'summary_shipping_cost': str(product.product.shipping_cost)
      }
      response.update(cost_summary)

    except Exception as e:
      response = {'exception': str(e)}
      Email(message="error in saveProduct ajax: "+str(e)).sendTo(Tom.email)

  else:
    response['problem'] = "not GET"

  return HttpResponse(simplejson.dumps(response), mimetype='application/json')
  #return HttpResponse(response['exception'])
