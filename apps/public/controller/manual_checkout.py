from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from apps.admin.utils.decorator import access_required
from apps.admin.utils.exception_handling import ExceptionHandler
from apps.public.controller.forms import CheckoutForm
from apps.public.models import Cart
from apps.public.models.checkout import Checkout

@access_required('admin')
def createCheckout(request):
  from django.core.urlresolvers import reverse
  from apps.communication.controller.email_class import Email
  from settings.people import Dan, Tifawt

  try:
    cart = Cart.objects.get(id=request.session.get('cart_id'))

    if not (cart.email and cart.name and cart.shipping_address):
      raise Exception("Missing required form elements")

    checkout, created = Checkout.objects.get_or_create(cart=cart)
    checkout.is_manual_order = True
    checkout.save()
    manual_checkout = reverse('manual checkout edit', args=[checkout.public_id])
    manual_checkout_url = request.build_absolute_uri(manual_checkout)
    message = "To continue manual checkout go to: %s" % manual_checkout_url
    Email(message=message).sendTo([Dan.email,Tifawt.email]) #only send to trusted staff

    return HttpResponse(status=200)

  except Exception as e:
    ExceptionHandler(e, "on checkout.adminCheckout")
    return HttpResponse(status=400)

@access_required('admin')
def editCheckout(request, checkout_public_id):
  checkout = Checkout.objects.get(public_id=checkout_public_id)
  request.session['cart_id'] = checkout.cart.id

  checkout_form = CheckoutForm()
  try:
    for attribute in ['total_charge', 'total_discount', 'total_paid', 'total_refunded',
                      'receipt', 'notes', 'currency',]:
      checkout_form.fields[attribute].initial = getattr(checkout, attribute)
  except Exception as e:
    ExceptionHandler(e, "error on cart form")

  context = {'cart': checkout.cart, 'checkout_form': checkout_form}
  return render(request, 'checkout/manual_checkout.html', context)

@csrf_exempt
def saveCheckout(request): #ajax requests only
  checkout = Cart.objects.get(id=request.session.get('cart_id')).checkout

  for attribute in ['total_charge', 'total_discount', 'total_paid', 'total_refunded',
                    'receipt', 'notes', 'currency',]:
    if request.POST.get(attribute):
      setattr(checkout, attribute, request.POST.get(attribute))
  checkout.save()

  return redirect('confirmation', checkout.public_id)
