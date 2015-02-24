from datetime import datetime, timedelta
from django.db.models import Sum
from django.shortcuts import render
from apps.public.models.order import Order


def stats(request):
  countries = sorted(Order.objects.values('checkout__cart__country').distinct())
  months = []

  now_date = datetime.now()
  stats_end = datetime(2016, 1, 1)#datetime(now_date.year, now_date.month, 1)

  month_start, month_end = next_month_start_end(datetime(2014,1,1))
  while month_end < stats_end:

    month_orders = Order.objects.filter(shipped_at__gte=month_start).filter(shipped_at__lt=month_end)
    month = {'name': month_start.strftime('%Y %B')} #full month name, year
    month['total'] = month_orders.aggregate(Sum('shipping_charge'))['shipping_charge__sum']
    month['AI'] = (month_orders.filter(tracking_number__startswith="AI").aggregate(Sum('shipping_charge'))['shipping_charge__sum'] or 0)
    month['CP'] = (month_orders.filter(tracking_number__startswith="CP").aggregate(Sum('shipping_charge'))['shipping_charge__sum'] or 0) + (month_orders.filter(tracking_number__startswith="ED").aggregate(Sum('shipping_charge'))['shipping_charge__sum'] or 0)
    month['RR'] = (month_orders.filter(tracking_number__startswith="RR").aggregate(Sum('shipping_charge'))['shipping_charge__sum'] or 0)

    month['other'] = (month_orders.exclude(tracking_number__startswith="AI").exclude(tracking_number__startswith="CP").exclude(tracking_number__startswith="ED").exclude(tracking_number__startswith="RR").aggregate(Sum('shipping_charge'))['shipping_charge__sum'] or 0)


    month['USA'] = (month_orders.filter(checkout__cart__country__in=['US','USA','usa','United States','United States of America','UNITED STATES']).aggregate(Sum('shipping_charge'))['shipping_charge__sum'] or 0)

    month['Canada'] = (month_orders.filter(checkout__cart__country__in=['Canada','CA','CANADA']).aggregate(Sum('shipping_charge'))['shipping_charge__sum'] or 0)

    month['Australia'] = (month_orders.filter(checkout__cart__country__in=['Australia','AU','AUSTRALIA','AUSTRALIE']).aggregate(Sum('shipping_charge'))['shipping_charge__sum'] or 0)

    month['UnitedKingdom'] = (month_orders.filter(checkout__cart__country__in=['United Kingdom','UK','ENGLAND','U.K','England','Grande Bretagne','UNITED KINGDOM','Ireland']).aggregate(Sum('shipping_charge'))['shipping_charge__sum'] or 0)

    months.append(month)
    month_start, month_end = next_month_start_end(month_end)

  return render(request, 'stats/shipping.html', {
    'countries': countries,
    'months': months,
  })

def next_month_start_end(this_month_end):
  next_month_start = this_month_end
  following_month = this_month_end + timedelta(days=32)
  next_month_end = datetime(following_month.year, following_month.month, 1)
  return (next_month_start, next_month_end)