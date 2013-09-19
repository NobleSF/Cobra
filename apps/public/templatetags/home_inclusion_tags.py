from django import template
register = template.Library()

@register.inclusion_tag('home/homepage_products.html')
def homepage_products_tag():
  from django.utils import timezone
  from apps.seller.models import Product
  from apps.public.controller.product_ranking import getRankPoints

  products = (Product.objects.filter(sold_at=None,
                                    approved_at__lte=timezone.now(),
                                    active_at__lte=timezone.now(),
                                    seller__approved_at__lte=timezone.now(),
                                    seller__deactive_at=None,
                                    deactive_at=None))

  for p in products:
    p.points = getRankPoints(p)

  products = sorted(products, key=lambda p: p.points)
  products.reverse() #sort by points descending
  return {'products':products}

@register.inclusion_tag('home/product.html')
def product_tag(product):
  return {'product': product}

@register.inclusion_tag('home/search_bar.html')
def search_bar_tag(search_keywords=None):
  from apps.admin.models import Category

  return {'categories':Category.objects.all()}
