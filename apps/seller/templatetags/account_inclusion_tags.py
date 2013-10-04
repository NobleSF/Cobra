from django import template
register = template.Library()

@register.inclusion_tag('account/image.html')
def image_tag(image_id):
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
