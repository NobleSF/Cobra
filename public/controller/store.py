from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext

def home(request, seller_id):
  from seller.models import Seller
  seller = Seller.objects.get(id=seller_id)

  return render(request, 'store/home.html')
