from django import template
from apps.public.models import Rating

register = template.Library()

@register.inclusion_tag('products/product_review_row.html')
def product_review_row(product, admin_type):

  rating_subjects = [subject[1] for subject in Rating.SUBJECT_OPTIONS]

  return {'product': product,
          'rating_subjects':rating_subjects,
          'rating_values': range(1,6),
          'admin_type': admin_type
         }
