from django import template
register = template.Library()

@register.inclusion_tag('account/image.html')
def image_tag(image_id=None):
  from seller.models import Image
  try:
    if image_id is not None:
      image_url = Image.objects.get(id=image_id).thumb
    else:
      image_url = None
  except Exception as e:
    image_url = None
  return {'image_url': image_url}

@register.inclusion_tag('account/asset.html')
def asset_tag(image_form, asset_form, asset=None):
  from seller.models import Asset
  try:
    if asset is not None:
      asset_form.fields["asset_id"].initial = asset.id
      asset_form.fields["ilk"].initial = asset.ilk
      asset_form.fields["image_url"].initial = asset.image_id
      asset_form.fields["name"].initial = asset.name
      asset_form.fields["description"].initial = asset.description
      asset_form.fields["category"].initial = asset.category.all()

  except Exception as e:
    asset = None

  return {'asset':asset, 'asset_form':asset_form, 'image_form':image_form}
