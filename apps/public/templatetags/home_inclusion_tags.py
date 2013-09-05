from django import template
register = template.Library()

@register.inclusion_tag('home/homepage_products.html')
def homepage_products_tag():
  from datetime import datetime
  from apps.seller.models import Product

  products = (Product.objects.filter(sold_at=None,
                                    approved_at__lte=datetime.today(),
                                    active_at__lte=datetime.today(),
                                    deactive_at=None)
               .order_by('approved_at')
               .reverse()
             )

  top_products = []
  top_product_ids = [336,88,320,324,30,21,287,133,127,4,125,
                    16,122,60,44,29,155,136,327,97,113]

  #append top products to list in order by id
  for id in top_product_ids:
    try:
      product = products.filter(id=id)[0]
      top_products.append(product)
      products = products.exclude(id=id)
    except:pass

  #append all the leftovers
  for product in products:
    top_products.append(product)

  return {'products':top_products}

@register.inclusion_tag('home/product.html')
def product_tag(product):
  return {'product': product}

@register.inclusion_tag('home/search_bar.html')
def search_bar_tag(search_keywords=None):
  from apps.admin.models import Category

  return {'categories':Category.objects.all()}
