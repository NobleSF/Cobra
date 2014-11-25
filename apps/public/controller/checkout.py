from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from apps.admin.utils.exception_handling import ExceptionHandler
from apps.public.models.checkout import Checkout

@csrf_exempt
def stripe_checkout(request):
  import stripe
  from settings.settings import STRIPE_SECRET_KEY

  stripe_token = request.POST.get('stripeToken')
  #stripe_token_type = request.POST.get('stripeTokenType')
  #stripe_email = request.POST.get('stripeEmail')
  stripe.api_key = STRIPE_SECRET_KEY #initiate stripe

  checkout = Checkout(cart_id=request.session.get('cart_id'))
  if stripe_token:
    try:
      charge = stripe.Charge.create(
          amount=int(float(checkout.cart.summary()) * 100), # amount in cents, again
          currency="usd",
          card=stripe_token,
          description="payment to Anou"
      )
      checkout.payment_id = charge.get('id')
      checkout.checkout_data = charge

    except stripe.CardError, e:
      # The card has been declined
      print "card has been declined"
    except Exception as e:
      ExceptionHandler(e, 'in checkout.stripe_checkout')

  checkout.save()
  return redirect('confirmation', checkout.public_id)

def confirmation(request, checkout_id=None):
  checkout_id = checkout_id or request.GET.get('checkout_id')
  checkout = Checkout.objects.filter(Q(payment_id=checkout_id) | Q(public_id=checkout_id)).first()
  context = {'checkout': checkout}

  if checkout.is_manual_order:
    if request.session.get('cart_id') and checkout.cart.id == request.session.get('cart_id'):
      del request.session['cart_id']

  elif checkout.cart.wepay_checkout_id:
    wepay_data = checkout.getWepayCheckoutData() #return {} if no data available
    checkout.payment_data = wepay_data if wepay_data else checkout.payment_data

    if (checkout.payment_data.get('gross') and
        checkout.payment_data.get('state') in ['authorized', 'reserved', 'captured', 'refunded']):

      if request.session.get('cart_id') and checkout.cart.id == request.session.get('cart_id'):
        del request.session['cart_id']

      if checkout.payment_data.get('state') in ['refunded']:
        context['refund'] = True
    else:
      context['problem'] = "Payment on order is not complete."

  elif checkout.cart.stripe_charge_id:
    #pull updated stripe payment data
    if checkout.payment_data and checkout.payment_data.get('paid'):

      if request.session.get('cart_id') and checkout.cart.id == request.session.get('cart_id'):
        del request.session['cart_id']

      if checkout.payment_data.get('refunded'):
        context['refund'] = True

    else:
      context['problem'] = "Payment on order is not complete."

  else:
    context['problem'] = "Problem collecting your order information."
    #todo: email the customer that we are aware of the problem
    # if checkout.email:
    #   Email(message="Sorry for your trouble.").sendTo([checkout.email])

  return render(request, 'checkout/confirmation.html', context)
