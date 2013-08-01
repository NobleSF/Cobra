from django import template
register = template.Library()

@register.inclusion_tag('account/image.html')
def image_tag(image_id=None):
  from apps.seller.models import Image
  try:
    image_url = Image.objects.get(id=image_id).thumb_size

  except Exception as e:
    image_url = None
  return {'image_url': image_url}

@register.inclusion_tag('account/asset.html')
def asset_tag(image_form, asset_form, asset=None):
  from apps.seller.models import Asset
  try:
    asset_form.fields["asset_id"].initial     = asset.id
    asset_form.fields["ilk"].initial          = asset.ilk
    asset_form.fields["image_url"].initial    = asset.image_id
    asset_form.fields["name"].initial         = asset.name
    asset_form.fields["description"].initial  = asset.description
    asset_form.fields["category"].initial     = asset.categories.all()
    image_id = asset.image_id

  except Exception as e:
    asset = None
    image_id = None

  context = {
              'asset':      asset,
              'asset_form': asset_form,
              'image_form': image_form,
              'image_id':   image_id
            }

  return context
