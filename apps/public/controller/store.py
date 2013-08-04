from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.template import RequestContext

def home(request, seller_id):
  from apps.seller.models import Seller

  try:
    store = Seller.objects.get(id=seller_id)
    store.artisans = store.asset_set.filter(ilk='artisan')

    context = {'store':store}

  except Seller.DoesNotExist:
    return Http404

  except Exception as e:
    context = {'except':e}

  return render(request, 'store.html', context)
