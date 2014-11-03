from django.http import HttpResponse
from django.template.loader import render_to_string
from settings.settings import PRODUCTION, STAGE

def orders(request):
  from apps.public.models.order import Order
  if PRODUCTION:
    test_checkout_id = '62513453'
  elif STAGE:
    test_checkout_id = '1245728081'
  else:
    test_checkout_id = '1535282677'

  if request.method == 'GET':
    checkout_id = request.GET.get('checkout_id', None)
  checkout_id = int(checkout_id) if checkout_id else test_checkout_id

  try:
    orders = Order.objects.filter(cart__wepay_checkout_id=checkout_id)
  except:
    orders = Order.objects.filter(cart__anou_checkout_id=checkout_id)

  response = render_to_string('email/order/created/html_body.html', {'data':orders})
  response += "<br>"*6
  response += render_to_string('email/order/confirmed/html_body.html', {'data':orders[0]})
  response += "<br>"*6
  response += render_to_string('email/order/shipped/html_body.html', {'data':orders[0]})
  response += "<br>"*6
  #response += render_to_string('email/order/followup/html_body.html', {'data':orders[0]})

  return HttpResponse(response)

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
