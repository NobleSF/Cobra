from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from apps.admin.utils.exception_handling import ExceptionHandler
from apps.public.controller.forms import CartForm
from apps.public.models import Cart
from apps.seller.models.product import Product

def cart(request):
  try:
    cart, created = Cart.objects.get_or_create(id=request.session.get('cart_id'))
  except Exception as e:
    ExceptionHandler(e, "error on cart")
    cart = Cart()

  if cart.checked_out: #if paid, start a new empty cart
    cart = Cart()

  cart.save()
  request.session['cart_id'] = cart.id

  cart_form = CartForm()
  try:
    for attribute in ['email', 'name', 'address_name', 'address1', 'address2',
                      'city', 'state', 'postal_code', 'country']:
      cart_form.fields[attribute].initial = getattr(cart, attribute)
  except Exception as e:
    ExceptionHandler(e, "error on cart form")

  context = {'cart': cart, 'cart_form': cart_form}

  if not 'admin_id' in request.session:
    from settings import STRIPE_PUBLIC_KEY
    context['STRIPE_PUBLIC_KEY'] = STRIPE_PUBLIC_KEY

  return render(request, 'checkout/cart.html', context)

def cartAdd(request, product_id):
  cart, created = Cart.objects.get_or_create(id=request.session.get('cart_id'))

  try:
    cart.addItem(Product.objects.get(id=product_id))

  except Exception as e:
    ExceptionHandler(e, "in checkout.cartAdd")
    #return to where you came from
    if 'HTTP_REFERER' in request.META:
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

  finally:
    request.session['cart_id'] = cart.id
    return redirect('cart')

def cartRemove(request, product_id):
  cart, created = Cart.objects.get_or_create(id=request.session.get('cart_id'))

  if not created:
    try:
      cart.removeItem(Product.objects.get(id=product_id))
    except Exception as e:
      ExceptionHandler(e, "in checkout.cartRemove")

  return redirect('cart')

@csrf_exempt
def cartSave(request): #ajax requests only
  try:
    cart = Cart.objects.get(id=request.session.get('cart_id'))
    attribute, value = request.POST.get('name'), request.POST.get('value')

    if attribute and value:
      setattr(cart, attribute, str(value))
      cart.save()
    return HttpResponse(status=200)#ok

  except Exception as e:
    ExceptionHandler(e, "in checkout.cartSave")
    return HttpResponse(status=400)#bad data


