from django import template
register = template.Library()

@register.inclusion_tag('home/homepage_products.html')
def homepage_products_tag():
  from django.utils import timezone
  from datetime import timedelta
  from apps.seller.models import Product
  from apps.public.controller.product_ranking import updateRankings

  products = (Product.objects.filter(sold_at=None,
                                    approved_at__lte=timezone.now(),
                                    active_at__lte=timezone.now(),
                                    seller__approved_at__lte=timezone.now(),
                                    seller__deactive_at=None,
                                    deactive_at=None))

  yesterday = timezone.now() - timedelta(days=1)

  for p in products:
    try:
      if p.ranking.updated_at <= yesterday:
        updateRankings(p, except_ratings=True)
    except:
      updateRankings(p)

  products = sorted(products, key=lambda p: p.ranking.weighted_average)
  products.reverse() #sort by points descending

  return {'products':products}

@register.inclusion_tag('home/product.html')
def product_tag(product):
  return {'product':product}

@register.inclusion_tag('home/search_bar.html')
def search_bar_tag(search_keywords=None):
  from apps.admin.models import Category
  categories = {}

  parent_categories = [c for c in Category.objects.all() if c.is_parent_category]
  for parent in parent_categories:
    categories[parent.plural_name] = [sub.plural_name for sub in parent.sub_categories.all()]

  return {'categories': categories}
