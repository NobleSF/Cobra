from django import template
register = template.Library()

@register.inclusion_tag('home/homepage_products.html')
def homepage_products_tag():
  from apps.seller.models.product import Product

  products = Product.objects.for_sale().exclude(ranking=None)
  #sort by average ranking points, descending
  products = sorted(products, key=lambda p: p.ranking.weighted_average)
  products.reverse()
  return {'products':products}

@register.inclusion_tag('home/product.html')
def product_tag(product):
  return {'product':product}

@register.inclusion_tag('home/search_bar.html')
def search_bar_tag(search_keywords=None):
  from apps.common.models.category import Category
  categories = {}

  parent_categories = [c for c in Category.objects.all() if c.is_parent_category]
  for parent in parent_categories:
    categories[parent.plural_name] = [sub.plural_name for sub in parent.sub_categories.all()]

  return {'categories': categories}
