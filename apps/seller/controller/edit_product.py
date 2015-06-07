import json
import re
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from apps.admin.utils.decorator import access_required
from apps.admin.utils.exception_handling import ExceptionHandler
from apps.seller.models.shipping_option import ShippingOption
from apps.seller.models.product import Product
from apps.seller.models.asset import Asset
from apps.admin.models.color import Color
from settings import CLOUDINARY

@access_required('admin or seller')
@csrf_exempt
def edit(request, product_id=None):

  try:
    product_id = product_id if product_id else request.POST.get('product_id')

    if request.session.get('admin_type') in ['master','country','trainer']:
      product = Product.objects.get(id=product_id)
    else:
      product = Product.objects.get(id=product_id,
                                    seller_id=request.session['seller_id'])

  except Exception as e:
    error_message = "in inventory.edit with product %s" % str(product_id)
    ExceptionHandler(e, error_message)
    return redirect('seller:home')

  # GET REQUEST FOR EDIT PRODUCT PAGE
  if request.method == 'GET':
    context = {
      'product':    product,
      'CLOUDINARY': CLOUDINARY,
    }
    return render(request, 'edit_product/edit.html', context)

  # POST REQUEST TO UPDATE A PRODUCT
  elif request.method == 'POST':
    response = {}
    try:
      if request.session.get('admin_type') in ['master','country','trainer']:
        product = Product.objects.get(id=request.POST.get('product_id'))
      else:
        product = Product.objects.get(id=request.POST.get('product_id'),
                                      seller_id = request.session['seller_id'])

      if request.POST.get('activate') == "yes":
        product.is_active = True
        product.save()

      name  = request.POST.get('name', None)
      value = request.POST.get('value', None)
      # remove non-digits, round to nearest integer
      value = int(round(float(re.sub(r"\D", "", value)))) if value else None
      value = value/100 if value > 70000 else value

      if   name == 'price':   product.price   = value
      elif name == 'length':  product.length  = value
      elif name == 'width':   product.width   = value
      elif name == 'height':  product.height  = value
      elif name == 'weight':  product.weight  = value

      elif name == 'asset':
        try:
          asset = (Asset.objects.filter(seller=product.seller) #asset belongs to seller
                   .get(id=request.POST.get('asset_id')))

          if request.POST.get('selected') == 'yes':
            product.assets.add(asset)
          else:
            product.assets.remove(asset)

        except Exception as e:
          response['asset'] = str(e)
          ExceptionHandler(e, message="in edit_product.edit asset", no_email=True)
        else:
          response['asset'] = "change saved"

      elif name == 'color':
        try:
          color = Color.objects.get(id=request.POST.get('color_id'))

          if request.POST.get('selected') == 'yes':
            product.colors.add(color)
          else:
            product.colors.remove(color)

        except Exception as e:
          response['color'] = str(e)
          ExceptionHandler(e, message="in edit_product.edit color", no_email=True)
        else:
          response['color'] = "change saved"

      elif name == 'shipping_option':
        try:
          shipping_option = ShippingOption.objects.get(
                              id=request.POST.get('shipping_option_id'))

          if request.POST.get('selected') == 'yes':
            product.shipping_options.add(shipping_option)
          else:
            product.shipping_options.remove(shipping_option)

        except Exception as e:
          response['shipping_option'] = str(e)
          ExceptionHandler(e, message="in edit_product.edit shipping_option", no_email=True)
        else:
          response['shipping_option'] = "change saved"

      else: #product unchanged
        try: response['nothing'] = "did nothing with name: %s, value: %d" % (name, value)
        except: pass

      # include name, value in response
      response['name'], response['value'] = name, value

      # activate, or deactivate product
      if name == 'activate' and product.is_complete:
        product.is_active = True
        response['activated'] = True
      elif product.is_active:
        product.active_at = product.deactive_at = None

      cost_summary = {
        'summary_price': str(product.price) if product.price else "",
        'summary_shipping_cost': str(product.shipping_cost)
      }
      response.update(cost_summary)
      response['is_complete'] = product.is_complete

      #save product only at the very end
      if not product.is_sold:
        product.is_approved = False
      product.save()

    except Exception as e:
      ExceptionHandler(e, "in inventory.saveProduct", no_email=True)
      response = {'exception': str(e)}

  else:
    response = {'problem': "not GET or POST"}

  return HttpResponse(json.dumps(response), content_type='application/json')
  #return HttpResponse(response['exception'])
