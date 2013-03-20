from django import template
register = template.Library()

@register.inclusion_tag('account/image.html')
def image(image_id):
  from seller.models import Asset, Image
  #asset = get_or_none(Asset, seller=seller_id, ilk=asset_ilk, rank=asset_rank)
  try:
    if asset is not None:
      image = Image.objects.get(id=asset.image).thumb
    else:
      image = None

  except Exception as e:
    image = None

  return {'image': image}


def get_or_none(model, **kwargs):
  try:
    return model.objects.get(**kwargs)
  except model.DoesNotExist:
    return None
