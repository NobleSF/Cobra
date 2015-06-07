from django import template
from math import ceil as roundUp
register = template.Library()

@register.inclusion_tag('edit_product/photo_upload.html')
def photo_upload_tag(product, rank):

  try: photo = product.photos.get(rank=rank)
  except: photo = None

  return {'product':product,
          'rank':rank,
          'photo':photo
         }

@register.inclusion_tag('edit_product/product_asset_choosers/asset_chooser.html')
def asset_chooser_tag(product, ilk):
  try:
    # get assets that belong to the seller, are of this ilk, and have an image
    assets = product.seller.asset_set.filter(ilk=ilk).filter(image__gte=1)
    for asset in assets:
      asset.selected = True if product.assets.filter(id=asset.id).exists() else False

  except:
    assets = None

  return {'assets':assets, 'ilk':ilk}

@register.inclusion_tag('edit_product/product_asset_choosers/shipping_option_chooser.html')
def shipping_option_chooser_tag(product):
  try:
    shipping_options = product.seller.country.shippingoption_set.all()
    for s_o in shipping_options:
      s_o.selected = True if product.shipping_options.filter(id=s_o.id).exists() else False

  except:
    shipping_options = None

  return {'shipping_options':shipping_options}

@register.inclusion_tag('edit_product/product_asset_choosers/color_chooser.html')
def color_chooser_tag(product):
  from apps.common.models.color import Color
  try:
    colors = Color.objects.all()
    for color in colors:
      color.selected = True if product.colors.filter(id=color.id).exists() else False

  except:
    colors = None

  return {'colors':colors}
