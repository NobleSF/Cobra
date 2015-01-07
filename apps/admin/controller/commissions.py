from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import dateformat, timezone
from django.views.decorators.csrf import csrf_exempt
from apps.admin.utils.exception_handling import ExceptionHandler
from settings.settings import CLOUDINARY
from apps.admin.utils.decorator import access_required
from apps.public.models import Commission

@access_required('admin')
def commissions(request):
  context = {'commissions_requested':   Commission.objects.requested().order_by('-created_at'),
             'commissions_in_progress': Commission.objects.in_progress().order_by('-created_at'),
             'commissions_completed':   Commission.objects.completed().order_by('-created_at'),
            }
  return render(request, 'commissions/commissions.html', context)

@access_required('admin')
@csrf_exempt
def commission(request, commission_id):
  if request.method == "POST":
    element = request.POST.get('name')
    value = request.POST.get('value')
    try:
      commission = Commission.objects.get(id=commission_id)
      if request.POST.get('base_product_id'):
        commission.base_product_id = int(request.POST['base_product_id'])
        commission.save()
        return redirect('admin:commission', commission.id)
      elif element == value == "cancel":
        commission.canceled = True
      else:
        commission.update(element, value)

      commission.save()
      return HttpResponse(200)#ok
    except Exception as e:
      ExceptionHandler(e, "in commissions.commission, saving commission details")
      return HttpResponse(500)#error

  elif request.method == "GET":
    context = {'commission':  Commission.objects.get(id=commission_id),
               'CLOUDINARY':  CLOUDINARY}
    return render(request, 'commissions/commission.html', context)

@access_required('admin')
def create(request):
  commission = Commission.objects.create()
  return redirect('admin:commission', commission.id)

@access_required('admin')
def find_commission(request): #search for commission based on POST params
  try:
    commission = Commission.objects.get(id=request.POST.get('commission_id'))
    return redirect('admin:commission', commission.id)
  except:
    return redirect('admin:commissions')

@access_required('admin')
@csrf_exempt #find a way to add csrf
def imageFormData(request):
  import json
  from apps.seller.controller.cloudinary_upload import createSignature
  from apps.seller.models.upload import Upload

  if request.method == "POST" and 'order_id' in request.POST:
    try:
      commission = Commission.objects.get(id=request.POST['commission_id'])
      timestamp   = dateformat.format(timezone.now(), u'U')#unix timestamp

      #uniquely name every image e.g. "seller23_order123_receipt_time1380924180"
      image_id  = "commission"+str(commission.id)
      image_id += "_time"+str(timestamp)
      tags = "requirement,commission%d" % commission.id

      #save as a pending upload
      Upload.objects.get_or_create(public_id = image_id)

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

      return HttpResponse(json.dumps(form_data), content_type='application/json')

    except Exception as e:
      ExceptionHandler(e, "in commission.imageFormData")
      return HttpResponse(status=500)#server error

  else:
    return HttpResponse(status=402)#bad request, payment required
