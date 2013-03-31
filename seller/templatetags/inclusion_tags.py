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
