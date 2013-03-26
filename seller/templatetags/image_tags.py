from django import template
register = template.Library()

@register.inclusion_tag('account/image.html')
def image(image_id=None):
  from seller.models import Asset, Image
  try:
    if asset is not None:
      image = Image.objects.get(id=asset.image)
    else:
      image = None

  except Exception as e:
    image = None

  return {'image': image}
