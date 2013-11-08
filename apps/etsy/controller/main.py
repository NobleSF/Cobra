from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from apps.etsy import api
from apps.etsy.controller.oauth import EtsyOAuthClient as OAuth
from apps.seller.models import Seller

def test(request):
  return render(request, 'test.html')

