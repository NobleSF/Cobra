from django.http import HttpResponse
from django.shortcuts import render
from apps.admin.controller.decorator import access_required
from django.contrib import messages
from apps.public.models import Order

@access_required('admin')
def allOrders(request):
  from apps.communication.controller.order_events import getCustomerAddressFromOrder

  orders = Order.objects.all().order_by('created_at').reverse()[:30]
  for order in orders:
    order.shipping_address = getCustomerAddressFromOrder(order)

  context = {'orders': orders}
  return render(request, 'orders/all_orders.html', context)

@access_required('admin')
def priceCalculator(request):
  from apps.seller.models import Product

  context = {}
  if request.method == "POST":
    try:
      product = Product.objects.get(id=request.POST.get('product_id'))

      context = {
        'product_id': product.id,
        'anou_price': product.display_price,
        'etsy_price': product.etsy_price,
        'ebay_price': product.ebay_price,
      }
    except Product.DoesNotExist:
      context['problem'] = "No Product with that ID"

    except Exception as e:
      context['problem'] = str(e)


  return render(request, 'orders/price_calculator.html', context)
