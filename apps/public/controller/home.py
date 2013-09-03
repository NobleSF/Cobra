from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils import simplejson
from datetime import datetime

def home(request):
  from apps.seller.models import Product

  products = (Product.objects.filter(sold_at=None,
                                    approved_at__lte=datetime.today(),
                                    active_at__lte=datetime.today(),
                                    deactive_at=None)
               .order_by('approved_at')
               .reverse()
             )

  context = {'products':products}
  return render(request, 'home/home.html', context)

def search(request, collection=None, category=None, color=None):
  from apps.seller.models import Product
  products = Product.objects.all()

  #for keyword in keywords:
  #  keyword = str(keyword)
  #  if keyword in colors:
  #    products = products.filter(product.color.name=keyword)
  #  if keyword in catagories:
  #    products = products.filter(product.category.name=keyword)
  #  if keyword in countries:
  #    products = products.filter(product.seller.country.name=keyword)
  #  if keyword in rating:#matches rating regex
  #    products = products.filter(product.rating >= keyword)

  search_keywords = {
    'collection':collection,
    'category':category,
    'color':color
  }

  context = {'products':products, 'search_keywords':search_keywords}
  return render(request, 'home/search.html', context)

def top_stores(request):
  return render(request, 'home/top_stores.html')

def about(request):
  return render(request, 'home/about.html')

def faq(request):
  return render(request, 'home/faq.html')

def contact(request):
  return render(request, 'home/contact.html')

def subscribe(request): #ajax requests only
  from django.db import IntegrityError
  from apps.communication.models import Subscription
  try:
    subscription = Subscription(email=request.GET.get('email'))
    if request.GET.get('name'):
      subscription.name = request.GET.get('name')
    subscription.save()
    response = {'success': "%s is subscribed" % subscription.email}

  except IntegrityError: #already subscribed
    if request.GET.get('name'):
      subscription = Subscription.objects.get(email=request.GET.get('email'))
      subscription.name = request.GET.get('name')
      subscription.save()
    response = {'success': "%s already subscribed" % subscription.email}

  except Exception as e:
    response = {'exception': str(e)}

  return HttpResponse(simplejson.dumps(response), mimetype='application/json')

def test_meta(request):
  values = request.META.items()
  values.append(['path', request.path])
  values.append(['host', request.get_host()])
  values.append(['full path', request.get_full_path()])
  values.append(['is secure', request.is_secure()])
  values.sort()
  html = []
  for k, v in values:
    html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
  return HttpResponse('<table>%s</table>' % '\n'.join(html))
