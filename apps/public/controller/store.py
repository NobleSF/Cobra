from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.core.urlresolvers import reverse
from apps.admin.utils.exception_handling import ExceptionHandler
from django.utils import timezone

def home(request, seller_id):
  from apps.seller.models import Seller

  try:
    store = Seller.objects.get(id=seller_id)
    store.artisans = store.asset_set.filter(ilk='artisan')

    products = (store.product_set.filter(sold_at=None,
                                         approved_at__lte=timezone.now(),
                                         deactive_at=None)
                .order_by('approved_at').reverse())

    sold_products = (store.product_set.filter(sold_at__lte=timezone.now(),
                                         approved_at__lte=timezone.now(),
                                         deactive_at=None)
                .order_by('sold_at').reverse())

    context = {'store':store, 'products':products, 'sold_products':sold_products}

  except Seller.DoesNotExist:
    raise Http404

  except Exception as e:
    ExceptionHandler(e, "in store.home")
    context = {'exception', str(e)}

  return render(request, 'store.html', context)
