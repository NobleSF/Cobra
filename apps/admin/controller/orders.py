from django.http import HttpResponse
from django.shortcuts import render
from apps.admin.utils.decorator import access_required
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
