from django import template
register = template.Library()

@register.inclusion_tag('products/product_review_row.html')
def product_review_row(product):
  from apps.admin.models import RatingSubject
  rating_subjects = RatingSubject.objects.all()

  return {'product': product,
          'rating_subjects':rating_subjects,
          'rating_values': range(1,6)
         }
