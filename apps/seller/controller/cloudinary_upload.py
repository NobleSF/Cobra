from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils import simplejson, timezone, dateformat
from apps.admin.utils.decorator import access_required
from apps.admin.utils.exception_handling import ExceptionHandler
from django.views.decorators.csrf import csrf_exempt
from apps.seller.models import Upload, Image, Photo
from settings.settings import CLOUDINARY
#from django.core.cache import cache

@csrf_exempt
def completeUpload(request):#for cloudinary to post info on completed uploads
  try:
    request_data = simplejson.loads(request.body)
    upload = Upload.objects.get(public_id = request_data.get('public_id'))
    if request_data.get('url').endswith(upload.public_id+'.jpg'):
      upload.complete_at = timezone.now()
      upload.url = request_data.get('url')
      upload.save()

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
  from apps.seller.models import Asset, Seller
  try:
    upload = Upload.objects.get(public_id = request.GET['public_id'])
    if upload.is_complete:
      image = Image(original=upload.url)
      image.save()

      if request.GET['ilk'] == 'seller':
        seller = Seller.objects.get(id=request.session['seller_id'])
        seller.image = image
        seller.save()

      else: #asset
        asset, is_new = Asset.objects.get_or_create(
                          seller_id = request.session['seller_id'],
                          ilk = request.GET['ilk'],
                          rank = request.GET['rank']
                        )

        asset.image = image
        asset.save()

      response = {'thumb_url': image.thumb_size}
      return HttpResponse(simplejson.dumps(response),
                          mimetype='application/json',
                          status='200')

    else:
      #todo:
      #cache.set('check_'+request.GET['public_id'], 300) #5 minutes
      return HttpResponse("did not find upload", status='204')

  except Exception as e:
    ExceptionHandler(e, "in cloudinary_upload.checkImageUpload", sentry_only=True)
    response = {'exception':str(e)}
    return HttpResponse(simplejson.dumps(response),
                        mimetype='application/json',
                        status='500')

@access_required('seller')
@csrf_exempt
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
  #todo: handle exceptions?

@access_required('seller')
@csrf_exempt
def checkPhotoUpload(request):#for our JS to check upload status and get thumb_url todo:cache response
  from apps.seller.controller.product_class import Product
  try:
    upload = Upload.objects.get(public_id = request.GET['public_id'])
    if upload.is_complete:
      request.product_id = request.GET['product_id']
      product = Product(request)

      photo = product.addPhoto(upload.url, request.GET['rank'])
      response = {'thumb_url': photo.thumb_size}

      return HttpResponse(simplejson.dumps(response),
                          mimetype='application/json',
                          status='200')
    else:
      return HttpResponse("did not find upload", status='204')

  except Exception as e:
    ExceptionHandler(e, "in cloudinary_upload.checkPhotoUpload", sentry_only=True)
    response = {'exception':str(e)}
    return HttpResponse(simplejson.dumps(response),
                        mimetype='application/json',
                        status='500')

@access_required('admin or seller')
@csrf_exempt
def photoFormData(request):
  if request.method == "POST":
    seller_id   = request.session['seller_id']
    product_id  = request.POST['product']
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
  return HttpResponse(simplejson.dumps(form_data), mimetype='application/json')
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
