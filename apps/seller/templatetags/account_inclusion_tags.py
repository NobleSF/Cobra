from django import template
register = template.Library()

@register.inclusion_tag('account/asset.html')
def asset_tag(asset_form, asset=None):
  from apps.seller.models import Asset
  try:
    asset_form.fields["ilk"].initial            = asset.ilk
    asset_form.fields["rank"].initial           = asset.rank
    asset_form.fields["name"].initial           = asset.name
    asset_form.fields["name_ol"].initial        = asset.name_ol
    asset_form.fields["description"].initial    = asset.description
    asset_form.fields["description_ol"].initial = asset.description_ol
    asset_form.fields["phone"].initial          = asset.phone
    if asset.categories.count():
      asset_form.fields["category"].initial     = asset.categories.all()[0].id

  except Exception as e:
    asset = None
    image_id = None

  return {'asset':      asset,
          'asset_form': asset_form
         }

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
