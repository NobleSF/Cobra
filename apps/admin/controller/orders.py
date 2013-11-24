from django.http import HttpResponse
from django.shortcuts import render
from apps.admin.utils.decorator import access_required
from django.contrib import messages
from apps.public.models import Order

@access_required('admin')
def allOrders(request):
  orders = Order.objects.all().order_by('created_at').reverse()[:50]

  context = {'orders': orders}
  return render(request, 'orders/all_orders.html', context)

@access_required('admin')
def order(request, order_id):
  from apps.communication.controller.order_events import getCustomerAddressFromOrder
  order = Order.objects.get(id=order_id)
  order.shipping_address = getCustomerAddressFromOrder(order)#todo: make this a model property

  return render(request, 'orders/order.html', {'order': order})

@access_required('admin')
def updateOrder(request):
  from django.utils import timezone

  if request.method == 'GET':
    order_id = request.GET.get('order_id')
    action = request.GET.get('action')

    order = Order.objects.get(id=order_id)

    if action == "seller paid":
      order.seller_paid_at = timezone.now()

    order.save()
    return HttpResponse(status=200)#OK

  else:
    return HttpResponse(status=402)#bad request
