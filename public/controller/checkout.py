from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext

def cart(request, username):
  return render(request, 'checkout/cart.html',
    {'username':username}
  )

def payment(request, username):
  return render(request, 'checkout/payment.html',
    {'username':username}
  )

def confirmation(request, username):
  return render(request, 'checkout/confirmation.html',
    {'username':username}
  )

def custom_order(request):
  return render(request, 'checkout/custom_order.html')
