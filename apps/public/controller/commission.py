import json
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from apps.admin.utils.exception_handling import ExceptionHandler
from apps.public.models import Commission, Customer
from apps.seller.models.product import Product
from settings.people import support_team
from apps.communication.controller.email_class import Email

def estimate(request):
  if request.GET.get('product_id'):
    commission = Commission(base_product_id=request.GET['product_id'])
    if request.GET.get('length') > 0:
      commission.length = int(request.GET['length'])
    if request.GET.get('width') > 0:
      commission.width  = int(request.GET['width'])

    price_estimate = commission.createPriceEstimate(save=False)
    response = {'display_price_estimate': price_estimate}
    return HttpResponse(json.dumps(response), content_type='application/json')

  else:
    return HttpResponse(status=500)

@require_POST
def propose(request):
  if all(item in request.POST for item in ['product_id', 'email', 'country']):

    customer, created = Customer.objects.get_or_create(email=request.POST['email'])
    customer.country = request.POST['country']
    customer.save()

    commission = Commission(base_product_id=request.POST['product_id'])
    commission.customer = customer
    commission.length = request.POST.get('length')
    commission.width = request.POST.get('width')
    commission.createPriceEstimate(),
    commission.createWeightEstimate()
    commission.save()

    try:
      data = {
        'product':        Product.objects.get(id=request.POST['product_id']),
        'country':        request.POST['country'],
        'email':          request.POST['email'],
        'size':           request.POST.get('size', ""),
        'quantity':       request.POST.get('quantity', ""),
        'description':    request.POST.get('description', ""),
        'estimate':       request.POST.get('estimate', ""),
        'commission':     commission,
        'customer':       customer,
      }

      recipient_email_list = [data['email'],] + [person.email for person in support_team]
      Email('custom_order/request', data).sendTo(recipient_email_list)
      return HttpResponse(status=200)

    except Exception as e:
      ExceptionHandler(e, "error in custom_order.createCustomOrder")
      return HttpResponse(status=500)

  else:
    return HttpResponse(status=400)

def create(request):
  commission = Commission.objects.get(id=request.GET['commission_id'])
  commission.product = commission.createProduct()
  context = {'commission': commission}
  #return redirect('commission')