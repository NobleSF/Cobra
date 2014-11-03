from django import template
register = template.Library()

@register.inclusion_tag('products/product_review_row.html')
def product_review_row(product, admin_type):
  from apps.admin.models.rating_subject import RatingSubject
  rating_subjects = RatingSubject.objects.all()

  return {'product': product,
          'rating_subjects':rating_subjects,
          'rating_values': range(1,6),
          'admin_type': admin_type
         }
