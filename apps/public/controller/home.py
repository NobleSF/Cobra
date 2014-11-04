import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_page

def home(request):
  return render(request, 'home/home.html')

@cache_page(176400) #49hrs an hour over homepage in-template cache
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
  return render(request, 'home/about.html')

def commonthread(request):
  return render(request, 'home/commonthread.html')

def commonthreadAddToCart(request, rug_name):
  from apps.seller.models.product import Product
  from apps.communication.controller.email_class import Email
  from settings.people import Tifawt, Dan, Tom

  rugs = {
    'opportunity':  [1860,1888,1889,1890,1891,1892,],
    'coexistence':  [1861,1882,1883,1884,1885,1886,],
    'mother':       [1862,1893,1894,1895,1896,1897,],
    'motherland':   [1863,1867,1868,1869,1870,1871,],
    'sacred':       [1864,1877,1878,1879,1880,1881,],
    'identity':     [1865,1872,1873,1874,1875,1876,],
  }

  try:
    buy_this_one = None
    for product_id in rugs[rug_name]:
      if not buy_this_one:
        product = Product.objects.get(id=product_id)
        if not product.is_sold:
          buy_this_one = product

    if buy_this_one:
      return HttpResponseRedirect(reverse('cart-add', args=[buy_this_one.id]))
    else:
      email = Email(message=("%s rug is sold out!!!" % rug_name),
                    subject=("%s sold out" % rug_name))
      email.sendTo([Tom.email, Dan.email, Tifawt.email,])
      return HttpResponseRedirect(reverse('commonthread'))

  except:
    return HttpResponseRedirect(reverse('commonthread'))

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
