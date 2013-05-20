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
  from apps.seller.models import Product, Photo, Asset

  context = {}

  try:
    product.name = product.assets.filter(ilk='product')[0].name # +" from " seller.city
    product.seller_name = product.seller.name

    #grab only tools and materials
    utilities = product.assets.filter(ilk='tool') | product.assets.filter(ilk='material')
    #put name of the first 3 utilities used in 'details' array
    product.details = []
    for utility in utilities: #[0:3]
      product.details.append(utility.name)

    #get artisan information
    artisan = product.assets.filter(ilk='artisan')[0]
    product.artisan_image = artisan.image.thumb
    product.artisan_name = artisan.name
  except:
    product.name = "product by Cooperative"
  context['product'] = product

  photo_objects = Photo.objects.filter(product=product)
  for rank in '0123':
    try:
      context['photo_'+rank] = photo_objects[int(rank)]
    except:
      pass

  return context

@register.inclusion_tag('home/search_bar.html')
def search_bar_tag(search_keywords=None):
  from apps.admin.models import Category, Color, Country

  #these should be cached queries!!
  colors = Color.objects.all()
  categories = Category.objects.all()
  countries = Country.objects.all()
  #cached queries!

  context = {
    'colors':colors,
    'categories':categories,
    'countries':countries,
    'search_keywords':search_keywords
  }
