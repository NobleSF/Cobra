from django import template
register = template.Library()

@register.inclusion_tag('home/home_header.html')
def home_header_tag(request, style): #style options: full, mini, mobile
  (full, mini, mobile) = (False, False, False)

  if style == 'full':
    full = True
  elif style == 'mini':
    mini = True
  elif style == 'mobile':
    mobile = True

  return {'request':request, 'full': full, 'mini':mini, 'mobile':mobile}

@register.inclusion_tag('home/product.html')
def product_tag(product):
  from seller.models import Product, Photo, Asset

  context = {}
  try:
    product_type = product.assets.filter(ilk='product')[0].name
    artisan = product.assets.filter(ilk='artisan')[0].name
    product.name = product_type + " by " + artisan
  except:
    product.name = "thingy by whomever"

  context['product'] = product

  photo_objects = Photo.objects.filter(product=product)
  for rank in '0123':
    try:
      context['photo_'+rank] = photo_objects[int(rank)]
    except:
      pass

  return context
