import json

from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone, dateformat
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError

from apps.admin.utils.decorator import access_required
from apps.admin.utils.exception_handling import ExceptionHandler
from apps.seller.models import Product, Photo
from apps.seller.models.upload import Upload
from apps.seller.models.image import Image
from settings import CLOUDINARY


@csrf_exempt
def completeUpload(request):#for cloudinary to post info on completed uploads
  try:
    request_data = json.loads(request.body)
    upload = Upload.objects.get(public_id = request_data.get('public_id'))
    if request_data.get('url').endswith(upload.public_id+'.jpg'):
      upload.complete_at = timezone.now()
      upload.url = request_data.get('url')
      upload.save()

  except Upload.DoesNotExist as e:
    ExceptionHandler(e, "in cloudinary_upload.completeUpload, upload public id %s does not exist" % request_data.get('public_id'))
    return HttpResponse(status=406)#no upload with that public_id

  except Exception as e:
    ExceptionHandler(e, "in cloudinary_upload.completeUpload")
    return HttpResponse(str(e), status=500)

  else:
    #todo: cache.expire('check_'+request_data.get('public_id'))
    return HttpResponse(status=200)

def checkImageUpload(request):#for our JS to check upload status and get thumb_url
  #todo:
  #cached_response = cache.get('check_'+request.GET['public_id'])
  #if cached_response:
  #  return cached_response
  #else:
  from apps.seller.models.asset import Asset
  from apps.seller.models.seller import Seller

  if request.method != 'GET' or 'public_id' not in request.GET:
    return HttpResponse("public_id required", status=406)#Not acceptable

  else:
    try:
      upload = Upload.objects.get(public_id = request.GET['public_id'])
    except:
      return HttpResponse(status=410)#Gone, it failed, stop asking
    else:
      try:
        if upload.is_complete:
          image, created = Image.objects.get_or_create(original=upload.url)
          thumb_url = image.thumb_size

          if 'seller' == request.GET.get('ilk'):
            seller = Seller.objects.get(id=request.session['seller_id'])
            seller.image = image
            seller.save()

          elif 'ilk' in request.GET: #asset
            asset, created = Asset.objects.get_or_create(
                              seller_id = request.session['seller_id'],
                              ilk = request.GET['ilk'],
                              rank = request.GET['rank']
                            )

            asset.image = image
            asset.save()

          elif 'order_id' in request.GET:#order receipt
            from apps.public.models.order import Order
            order = Order.objects.get(id=request.GET['order_id'])
            order.seller_paid_receipt = image
            order.save()

          elif 'commission_id' in request.GET:#commission requirement or progress image
            from apps.commission.models.commission import Commission
            commission = Commission.objects.get(id=request.GET['commission_id'])
            if request.GET['image_or_photo'] == 'image':
              commission.requirement_images.add(image)
            elif request.GET['image_or_photo'] == 'photo':
              photo = Photo(original = image.original)
              photo.product = commission.product
              photo.is_progress = True
              photo.save()
              thumb_url = photo.thumb_size

          response = {'thumb_url': thumb_url}
          return HttpResponse(json.dumps(response),
                              content_type='application/json',
                              status='200')

        else:
          #todo:
          #cache.set('check_'+request.GET['public_id'], 300) #5 minutes
          return HttpResponse("did not find upload", status='204')

      except Exception as e:
        ExceptionHandler(e, "in cloudinary_upload.checkImageUpload", no_email=True)
        response = {'exception':str(e)}
        return HttpResponse(json.dumps(response),
                            content_type='application/json',
                            status='500')

@access_required('seller')
@csrf_exempt #find a way to add csrf
def imageFormData(request):
  if request.method == "POST":
    seller_id   = request.session['seller_id']
    ilk         = request.POST['ilk']
    rank        = request.POST['rank']
    timestamp   = dateformat.format(timezone.now(), u'U')#unix timestamp

    #uniquely name every image e.g. "seller23_ilkartisan_rank1_time1380924180"
    image_id  = "seller"+str(seller_id)
    image_id += "_ilk"+str(ilk)
    image_id += "_rank"+str(rank)
    image_id += "_time"+str(timestamp)
    #tag image with seller_id and asset_ilk
    tags = "seller"+str(seller_id)+",asset"+str(ilk)

    #save as a pending upload
    try:
      Upload(public_id = image_id).save()
    except IntegrityError:
      pass

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
  #todo: handle exceptions?

@access_required('seller')
@csrf_exempt
def checkPhotoUpload(request): #js checks upload status and gets thumb_url
  #todo:cache response
  if request.method != 'GET' or 'public_id' not in request.GET:
    return HttpResponse("public_id required", status=406)#Not acceptable

  else:
    try:
      upload = Upload.objects.get(public_id = request.GET['public_id'])
    except:
      return HttpResponse(status=410)#Gone, it failed, stop asking
    else:
      try:
        if upload.is_complete:
          from apps.seller.models.photo import Photo

          photo, is_new = Photo.objects.get_or_create(
                            product_id = request.GET['product_id'],
                            rank = request.GET['rank'])

          photo.original = upload.url
          photo.save()

          response = {'thumb_url': photo.thumb_size}

          return HttpResponse(json.dumps(response),
                              content_type='application/json',
                              status='200')
        else:
          return HttpResponse("did not find upload", status='204')

      except Exception as e:
        ExceptionHandler(e, "in cloudinary_upload.checkPhotoUpload", no_email=True)
        response = {'exception':str(e)}
        return HttpResponse(json.dumps(response),
                            content_type='application/json',
                            status='500')

@access_required('admin or seller')
@csrf_exempt
def photoFormData(request):
  if request.method == "POST":
    product_id  = request.POST['product']
    if request.session.get('admin_id'):
      seller_id = Product.objects.get(id=product_id).seller_id
    else:
      seller_id = request.session['seller_id']
    rank        = request.POST['rank']
    timestamp   = dateformat.format(timezone.now(), u'U')#unix timestamp

    #uniquely name every photo e.g. "seller12_product123_rank1_time1380924180"
    photo_id  = "seller"+str(seller_id)
    photo_id += "_product"+str(product_id)
    photo_id += "_rank"+str(rank)
    photo_id += "_time"+str(timestamp)
    #tag photo with product_id and seller_id
    tags = "product"+str(product_id)+",seller"+str(seller_id)

    #save as a pending upload
    Upload(public_id = photo_id).save()

    form_data = {
      'public_id':        photo_id,
      'tags':             tags,
      'api_key':          CLOUDINARY['api_key'],
      'format':           CLOUDINARY['format'],
      'transformation':   CLOUDINARY['transformation'],
      'timestamp':        timestamp,
      'notification_url': request.build_absolute_uri(reverse('seller:complete upload'))
      #'http://localcobra.pagekite.me/seller/ajax/complete_up'
      #http://respondto.it/complete-upload
    }
    form_data['signature'] = createSignature(form_data)
  return HttpResponse(json.dumps(form_data), content_type='application/json')
  #todo: handle exceptions?

def createSignature(data):
  import hashlib
  #in alphabetical order by parameter name, then api_secret last
  cloudinary_string  = 'format='            + data['format']
  cloudinary_string += '&notification_url=' + data['notification_url']
  cloudinary_string += '&public_id='        + data['public_id']
  cloudinary_string += '&tags='             + data['tags']
  cloudinary_string += '&timestamp='        + data['timestamp']
  cloudinary_string += '&transformation='   + data['transformation']
  cloudinary_string += CLOUDINARY['api_secret']

  h = hashlib.new('sha1')
  h.update(cloudinary_string)
  return h.hexdigest()
