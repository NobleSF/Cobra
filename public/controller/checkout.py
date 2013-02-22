from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext

def cart(request, username):
  return render(request, 'public/checkout/cart.html',
    {'username':username}
  )

def payment(request, username):
  return render(request, 'public/checkout/payment.html',
    {'username':username}
  )

def confirmation(request, username):
  return render(request, 'public/checkout/confirmation.html',
    {'username':username}
  )
