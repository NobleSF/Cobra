from datetime import datetime
from django.shortcuts import render
from apps.admin.utils.decorator import access_required
from apps.public.models.order import Order

@access_required('admin')
def home(request):
  #request.session['admin_type'] = 'master'
  return render(request, 'admin_home.html', {})

def stats(request):
  today = datetime.now()
  beginning_of_time = datetime(2013, 10, 1)#August 1st, 2013 - launch of this app
  firsts_of_months = [beginning_of_time,]

  #create list of datetimes, firsts of all months from beginning_of_time until now
  first_of_month = beginning_of_time
  while first_of_month < today:
    first_of_month = getNextMonth(first_of_month)
    firsts_of_months.append(first_of_month)

  revenue_data = []

  for date in firsts_of_months[:-1]:#don't use last value (in future)
    orders = Order.objects.filter(created_at__gte=date, created_at__lt=getNextMonth(date))

    product_value = anou_fees = shipping_costs = revenue = 0

    for order in orders:
      if order.is_complete:
        product_value   += int(order.products_charge)
        anou_fees       += int(order.anou_charge)
        shipping_costs  += int(order.shipping_charge)
        revenue         += int(order.total_charge)

    revenue_data.append(
      [date.strftime('%m-%y'),
       {'product_value':  product_value,
        'anou_fees':      anou_fees,
        'shipping_costs': shipping_costs,
        'revenue':        revenue,
        'costs':          int(getCostsForMonth(date))}
       ])

  # product_activity = {}
  # first_of_month = datetime(today.year, today.month, 1)
  # product_activity['products_added'] = Product.objects.filter(
  #                                         approved_at__gte=first_of_month
  #                                       ).count()
  #
  # from apps.public.models.rating import Rating
  # from django.db.models import Avg
  # ratings = (Rating.objects.filter(
  #             product__active_at__lte=today,
  #             product__deactive_at=None,
  #             product__in_holding=False,
  #             product__approved_at__lte=today))
  #
  # avg_rating = ratings.aggregate(average=Avg('value'))['average']
  # avg_rating_before = (ratings
  #                       .exclude(product__updated_at__gte=first_of_month)
  #                       .aggregate(average=Avg('value'))
  #                     )['average']
  #
  # avg_rating_normalized = (avg_rating-1)/4 * 100
  # avg_rating_before_normalized = (avg_rating_before-1)/4 * 100
  #
  #
  # product_activity['avg_rating'] = int(avg_rating_normalized)
  # product_activity['avg_rating_change'] = int(((avg_rating_normalized-avg_rating_before_normalized)/avg_rating_before_normalized) * 100)

  context = {'revenue_data':revenue_data}#, 'product_activity':product_activity
  return render(request, 'stats.html', context)

def getNextMonth(date):#not smart to handle end-of-month limits (eg Feb 30th)
    year = date.year if date.month < 12 else date.year + 1
    month = date.month+1 if date.month < 12 else 1
    day = date.day
    return datetime(year, month, day)

def getCostsForMonth(date):
  costs = {
    2013: {
      8:  7843,
      9:  12603,
      10: 12005,
      11: 10967,
      12: 8400,
    },
    2014: {
      1:  8660,
      2:  8800,
      3:  9902,
      4:  6978,
      5:  10175,
      6:  6074,
      7:  9047,
      8:  9832,
      9:  0,
      10: 0,
      11: 0,
      12: 0
    },
    2015: {
      1:  0,
      2:  0,
      3:  0,
      4:  0,
      5:  0,
      6:  0,
      7:  0,
      8:  0,
      9:  0,
      10: 0,
      11: 0,
      12: 0
    },
    2016: {
      1:  0,
      2:  0,
      3:  0,
      4:  0,
      5:  0,
      6:  0,
      7:  0,
      8:  0,
      9:  0,
      10: 0,
      11: 0,
      12: 0
    },
  }

  return costs[date.year][date.month]
