from django.shortcuts import render, redirect
from apps.admin.utils.decorator import access_required
from django.contrib import messages

@access_required('admin')
def dashboard(request):
  from apps.seller.models import Product
  from django.utils import timezone
  from datetime import date
  context = {}
  try:
    first_of_month = date(timezone.now().year, timezone.now().month, 1)

    context['mtd_product_count'] = (Product.objects.filter(
                                      approved_at__gte=first_of_month)
                                    ).count()

    from apps.public.models import Rating
    from django.db.models import Avg
    ratings = (Rating.objects.filter(
                product__active_at__lte=timezone.now(),
                product__deactive_at=None,
                product__in_holding=False,
                product__approved_at__lte=timezone.now()))

    #todo: cache this
    avg_rating = ratings.aggregate(average=Avg('value'))['average']
    avg_rating_before_month = (ratings
                                .exclude(product__updated_at__gte=first_of_month)
                                .aggregate(average=Avg('value'))
                              )['average']

    context['avg_rating'] = avg = (avg_rating-1)/4 * 100
    context['avg_rating_before_month'] = before = (avg_rating_before_month-1)/4 * 100
    context['avg_rating_change'] = (avg - before)

  except: pass
  return render(request, 'dashboard.html', context)
