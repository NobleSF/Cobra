from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils import simplejson
from apps.admin.utils.decorator import access_required
from apps.admin.utils.exception_handling import ExceptionHandler
from django.views.decorators.csrf import csrf_exempt
from apps.seller.models import Seller, Product
from settings.people import Tom, Dan
from apps.communication.controller.email_class import Email

@csrf_exempt
def requestCustomOrder(request): #post with product_id, customer_email, message
  if request.method == 'POST' and request.POST.get('customer_email'):
    try:
      data = {
        'product':        Product.objects.get(id=request.POST['product_id']),
        'customer_email': request.POST['customer_email'],
        'message':        request.POST['message'],
      }

      Email('custom_order/request', data).sendTo([Dan.email, data['customer_email']])
      return HttpResponse(status=200)

    except Exception as e:
      ExceptionHandler(e, "error in custom_order.createCustomOrder")
      return HttpResponse(status=500)

  else:
    return HttpResponse(status=400)
