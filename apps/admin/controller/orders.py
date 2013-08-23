from django.http import HttpResponse
from django.shortcuts import render
from apps.admin.controller.decorator import access_required
from django.contrib import messages
from django.utils import simplejson
from datetime import datetime
from apps.public.models import Order

@access_required('admin')
def createOrder(request):
  return render(request, 'orders/create_order.html', {'form': SMSForm()})

def allOrders(request):

  orders = Order.objects.all().order_by('created_at').reverse()[:20]


  context = {
              'orders': orders
            }
  return render(request, 'orders/all_orders.html', context)


def allEmail():
  pass
