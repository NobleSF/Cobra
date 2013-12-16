from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from apps.admin.utils.decorator import access_required
from django.views.decorators.csrf import csrf_exempt
from apps.admin.utils.exception_handling import ExceptionHandler
from django.contrib import messages
from apps.public.models import Order
from settings.settings import CLOUDINARY

@access_required('admin')
def allOrders(request):
  orders = Order.objects.all().order_by('created_at').reverse()[:50]

  context = {'orders': orders}
  return render(request, 'orders/all_orders.html', context)

@access_required('admin')
def order(request, order_id):
  try:
    order = Order.objects.get(id=order_id)
    order.shipping_address = order.cart.shipping_address.replace('\n','<br>')

    return render(request, 'orders/order.html', {'order': order, 'CLOUDINARY':CLOUDINARY})
  except Exception as e:
    print str(e)
    return redirect('admin:all orders')

@access_required('admin')
def updateOrder(request):
  from django.utils import timezone

  if request.method == 'GET':
    order_id = request.GET.get('order_id')
    action = request.GET.get('action')

    order = Order.objects.get(id=order_id)

    if action == "seller paid":
      order.seller_paid_at = timezone.now()

    order.save()
    return HttpResponse(status=200)#OK

  else:
    return HttpResponse(status=402)#bad request


@access_required('admin')
@csrf_exempt #find a way to add csrf
def imageFormData(request):
  from django.utils import timezone, dateformat, simplejson
  from apps.seller.controller.cloudinary_upload import createSignature
  from apps.seller.models import Upload

  if request.method == "POST" and 'order_id' in request.POST:
    try:
      order = Order.objects.get(id=request.POST['order_id'])
      timestamp   = dateformat.format(timezone.now(), u'U')#unix timestamp

      #uniquely name every image e.g. "seller23_order123_receipt_time1380924180"
      image_id  = "seller"+str(order.seller.id)
      image_id += "_order"+str(order.id)
      image_id += "_receipt"
      image_id += "_time"+str(timestamp)
      #tag image with seller_id and asset_ilk
      tags = "seller"+str(order.seller.id)+",order"+str(order.id)+",receipt"

      #save as a pending upload
      Upload(public_id = image_id).save()

      form_data = {
        'public_id':        image_id,
        'tags':             tags,
        'api_key':          CLOUDINARY['api_key'],
        'format':           CLOUDINARY['format'],
        'transformation':   CLOUDINARY['transformation'],
        'timestamp':        timestamp,
        'notification_url': request.build_absolute_uri(reverse('seller:complete upload')),
      }
      form_data['signature'] = createSignature(form_data)

      return HttpResponse(simplejson.dumps(form_data), mimetype='application/json')

    except Exception as e:
      ExceptionHandler(e, "in orders.imageFormData")
      return HttpResponse(status=500)#server error

  else:
    return HttpResponse(status=402)#bad request
