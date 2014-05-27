from django import template
from math import ceil as roundUp
register = template.Library()

@register.inclusion_tag('inventory/product_detail.html')
def product_detail_tag(product):
  return {'product':product}

@register.inclusion_tag('inventory/sold_product_detail.html')
def sold_product_detail_tag(product):
  product.total_cost = product.shipping_cost + product.intl_price
  return {'product':product}
