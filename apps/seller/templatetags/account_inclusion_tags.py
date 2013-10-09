from django import template
register = template.Library()

@register.inclusion_tag('account/asset.html')
def asset_tag(image_form, asset_form, asset=None):
  from apps.seller.models import Asset
  try:
    #asset_form.fields["asset_id"].initial       = asset.id
    asset_form.fields["ilk"].initial            = asset.ilk
    asset_form.fields["rank"].initial           = asset.rank
    asset_form.fields["image_url"].initial      = asset.image_id
    asset_form.fields["name"].initial           = asset.name
    asset_form.fields["name_ol"].initial        = asset.name_ol
    asset_form.fields["description"].initial    = asset.description
    asset_form.fields["description_ol"].initial = asset.description_ol
    asset_form.fields["phone"].initial          = asset.phone
    if asset.categories.all():
      asset_form.fields["category"].initial     = asset.categories.all()[0]

  except Exception as e:
    asset = None
    image_id = None

  context = {
              'asset':      asset,
              'asset_form': asset_form,
              'image_form': image_form
            }

  return context

@register.inclusion_tag('account/image_upload.html')
def image_upload_tag(image_form, asset=None, seller=None):

  if asset:
    image_url = asset.image.thumb_size if asset.image else None
    image_form.fields['ilk'].initial  = asset.ilk
    image_form.fields['rank'].initial = asset.rank
  elif seller:
    image_url = seller.image.thumb_size if seller.image else None
    image_form.fields['ilk'].initial  = "seller"
    image_form.fields['rank'].initial = 0
  else:
    image_url = ""

  return {'image_form':image_form,
          'image_url':image_url
         }
