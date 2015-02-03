import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apps.admin.utils.exception_handling import ExceptionHandler
from apps.seller.models.product import Product
from settings.people import support_team
from apps.communication.controller.email_class import Email

def estimate(request):
  try:
    product = Product.objects.get(id=request.GET['product_id'])

    if product and product.weight and product.price:

      product.length = product.length if product.length else 1
      product.height = product.height if product.height else 1
      product.width  = product.width  if product.width  else 1
      old_volume = product.length * product.width * product.height

      #sort dimensions and update two biggest ones
      dimensions = [product.length, product.width, product.height]
      dimensions.sort() #sort numbers smallest to biggest
      dimensions.reverse() #reverse order, so now biggest first

      if request.GET.get('length') and int(request.GET['length']) > 0:
        dimensions[0] = int(request.GET['length'])
      if request.GET.get('width') and int(request.GET['width']) > 0:
        dimensions[1]  = int(request.GET['width'])

      #get ratio from volume difference
      new_volume = dimensions[0] * dimensions[1] * dimensions[2]
      ratio = float(new_volume)/old_volume

      #scale ratio with quantity
      if request.GET.get('quantity') and request.GET['quantity'] > 1:
        ratio = ratio * int(request.GET['quantity'])

      #use ratio to scale price, weight
      product.price = int(round(product.price * ratio))
      product.weight = int(round(product.weight * ratio))
      #increase weight a bit to bump estimate to next shipping price tier if close
      product.weight = int(round((product.weight * 1.05) + 100)) #add 5% + 100grams

      response = {'display_price_estimate': product.display_price}
      product.pk = None #DO NOT SAVE!!!
      return HttpResponse(json.dumps(response), content_type='application/json')

    else:
      return HttpResponse(status=500)

  except Exception as e:
    ExceptionHandler(e, "error in product.custom_order_estimate")
    return HttpResponse(str(e), status=500)


@csrf_exempt
def request(request):
  if request.method == 'POST' and request.POST.get('email'):
    try:
      data = {
        'product':        Product.objects.get(id=request.POST['product_id']),
        'country':        request.POST['country'],
        'email':          request.POST['email'],
        'size_imperial':  request.POST.get('size_imperial', ""),
        'size_metric':    request.POST.get('size_metric', ""),
        'quantity':       request.POST.get('quantity', ""),
        'description':    request.POST.get('description', ""),
        'estimate':       request.POST.get('estimate', ""),
      }

      recipient_email_list = [data['email'],] + [person.email for person in support_team]
      Email('custom_order/request', data).sendTo(recipient_email_list)
      return HttpResponse(status=200)

    except Exception as e:
      ExceptionHandler(e, "error in custom_order.createCustomOrder")
      return HttpResponse(status=500)

  else:
    return HttpResponse(status=400)
