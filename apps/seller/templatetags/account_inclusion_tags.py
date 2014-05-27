from django import template
register = template.Library()

@register.inclusion_tag('account/asset.html')
def asset_tag(asset_form, asset=None):
  from apps.seller.models.asset import Asset
  from apps.seller.controllers.forms import AssetCategoryForm
  asset_category_form = AssetCategoryForm()
  try:
    if asset.categories.count():
      asset_category_form.fields["category"].initial = asset.categories.all()[0].id
      asset_category_form.fields["category"].widget.attrs.update({
        'data-ilk':asset.ilk,
        'data-rank':asset.rank})

  except Exception as e:
    asset = None
    image_id = None

  return {'asset': asset, 'asset_category_form': asset_category_form}

@register.inclusion_tag('account/image_upload.html')
def image_upload_tag(asset=None, seller=None):

  if asset:
    image = asset.image
    (ilk, rank) = (asset.ilk, asset.rank)
  elif seller:
    image = seller.image
    (ilk, rank) = ('seller', 0)
  else:
    image = None
    (ilk, rank) = ('ilk', 'rank')

  return {'image': image,
          'ilk': ilk,
          'rank': rank
          }
