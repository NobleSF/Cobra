from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
import json
from django.views.decorators.cache import cache_page

def home(request):
  return render(request, 'browse.html')

def category(rewuest):
  return render(request, 'browse.html')

def listingGrid(request): #partial
  return render(request, 'partials/listing-grid.html')

def categoryGrid(request): #partial
  return render(request, 'partials/category-grid.html')

def listing(request): #partial
  return render(request, 'partials/listing.html')

def store(request): #partial
  return render(request, 'partials/store.html')

def category(request): #partial
  return render(request, 'partials/category.html')


@cache_page(176400) #49hrs
def loadProducts(request):
  from apps.seller.models.product import Product
  from django.template.loader import render_to_string

  if request.method == "GET" and request.GET.get('product_ids'):
    product_html = {}

    for product_id in request.GET.get('product_ids').split(','):
      product = Product.objects.get(id=product_id)
      html = render_to_string('home/product.html', {'product':product})
      product_html[str(product.id)] = html

    return HttpResponse(json.dumps(product_html), content_type='application/json')
  else:
    return HttpResponse(json.dumps({}), content_type='application/json')

def about(request):
  return render(request, 'about/base.html')

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
