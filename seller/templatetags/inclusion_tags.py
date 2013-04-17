from django import template
register = template.Library()

@register.inclusion_tag('account/image.html')
def image_tag(image_id=None):
  from seller.models import Image
  try:
    if image_id is not None:
      image = Image.objects.get(id=image_id).thumb
    else:
      image = None
  except Exception as e:
    image = None
  return {'image': image}

@register.inclusion_tag('inventory/photo_upload.html')
def photo_upload_tag(photo_form, rank, photos=None):
  from seller.models import Photo
  try:
    if photo_id is not None:
      photo_url = photos.filter(rank=rank).thumb_url
    else:
      photo_url = None
  except Exception as e:
    photo_url = None
  return {'photo_form':photo_form, 'photo_url':photo_url}

@register.inclusion_tag('account/asset.html')
def asset_tag(image_form, asset_form, asset=None):
  from seller.models import Asset
  try:
    if asset is not None:
      asset_form.fields["asset_id"].initial = asset.id
      asset_form.fields["ilk"].initial = asset.ilk
      asset_form.fields["image"].initial = asset.image_id
      asset_form.fields["name"].initial = asset.name
      asset_form.fields["description"].initial = asset.description
      asset_form.fields["category"].initial = asset.category.all()

  except Exception as e:
    asset = None

  return {'asset':asset, 'asset_form':asset_form, 'image_form':image_form}

@register.inclusion_tag('inventory/asset_chooser.html')
def asset_chooser_tag(request, ilk):
  from seller.models import Asset
  try:
    seller_id = request.session['seller_id']
    assets = Asset.objects.all().filter(seller_id=seller_id, ilk=ilk)

  except Exception as e:
    assets = None

  return {'assets':assets, 'ilk':ilk}

@register.inclusion_tag('inventory/shipping_option_chooser.html')
def shipping_option_chooser_tag(request):
  from seller.models import Seller, ShippingOption
  try:
    country = Seller.objects.get(id=request.session['seller_id']).country
    shipping_options = ShippingOption.objects.all().filter(country=country)

  except Exception as e:
    shipping_options = None

  return {'shipping_options':shipping_options}
