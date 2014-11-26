from datetime import timedelta

from django.db import models
from jsonfield import JSONField
from django.utils import timezone

from apps.admin.utils.exception_handling import ExceptionHandler
from apps.communication.controller.email_class import Email
from apps.public.models.cart import Cart
from settings.people import support_team

class Checkout(models.Model):
  public_id           = models.CharField(max_length=8, null=True, blank=True)#set by post_save signal
  cart                = models.OneToOneField(to=Cart, related_name='checkout')

  # id number assigned by the payment provider
  payment_id          = models.CharField(max_length=35, null=True, blank=True)
  #the data returned by our payment provider
  payment_data        = JSONField(null=True, blank=True)
  is_manual_order     = models.BooleanField(default=False)

  total_charge        = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
  total_discount      = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
  total_paid          = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
  total_refunded      = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
  currency            = models.CharField(max_length=3, default="USD")

  receipt             = models.TextField(blank=True, null=True)
  notes               = models.TextField(blank=True, null=True)

  #update history
  created_at          = models.DateTimeField(auto_now_add=True)
  updated_at          = models.DateTimeField(auto_now=True)


  # MODEL PROPERTIES
  @property
  def is_paid(self): return True if self.total_paid else False

  @property
  def email(self): return self.cart.email
  @property
  def name(self): return self.cart.name
  @property
  def address_name(self): return self.cart.address_name if self.cart.address_name else self.cart.name
  @property
  def address1(self): return self.cart.address1
  @property
  def address2(self): return self.cart.address2
  @property
  def city(self): return self.cart.city
  @property
  def state(self): return self.cart.state
  @property
  def postal_code(self): return self.cart.postal_code
  @property
  def country(self): return self.cart.country

  @property
  def shipping_address (self):
    if self.address1 or self.address2:
      address  = "%s\n" % (self.address_name or "")
      address += ("%s\n" % self.address1) if self.address1 else ""
      address += ("%s\n" % self.address2) if self.address2 else ""
      address += ("%s, " % self.city) if self.city else ""
      address += ("%s " % self.state) if self.state else ""
      address += self.postal_code if self.postal_code else ""
      address += ("\n%s" % self.country) if self.country else ""
      return address.upper()


  # MODEL FUNCTIONS
  def pullStripeData(self):
    #todo: use stripe api to reset our data
    if self.payment_id.startswith('ch_'):
      return self.payment_data
    else:
      return {}

  #@postpone
  def cleanupCarts(self):
    from apps.seller.models.product import Product

    try:
      time_1_hour_ago = timezone.now() - timedelta(hours=1)
      recently_purchased_products = Product.objects.filter(sold_at__gte=time_1_hour_ago)

      #remove sold products from any carts that have not checked out yet
      for product in recently_purchased_products:
        for item in product.items.all():
          if not item.cart.checked_out:
            item.delete()

    except Exception as e:
      ExceptionHandler(e, "error on checkout.cleanupCarts")

  def getWePayCheckoutData(self):#todo delete once finished with potential refunds
    from apps.wepay.api import WePay
    from settings.settings import WEPAY, PAYMENTS_PRODUCTION
    if not self.cart.wepay_checkout_id: return {}
    else:
      try:
        wepay = WePay(PAYMENTS_PRODUCTION, WEPAY['access_token'])
        wepay_response = wepay.call('/checkout', {
          'checkout_id': self.cart.wepay_checkout_id
        })
      except Exception as e:
        return {'error': e}
      else:
        self.payment_id = self.cart.wepay_checkout_id
        self.payment_data = wepay_response if wepay_response else self.payment_data
        self.save()

        #PAYMENT INFO
        self.total_charge     = wepay_response.get('amount')
        self.total_discount   = 0
        self.total_paid       = wepay_response.get('amount') if wepay_response.get('state') in ['captured', 'refunded'] else 0
        self.total_refunded   = wepay_response.get('amount_refunded')

        #SHIPPING ADDRESS
        if not wepay_response.get('shipping_address'):
          wepay_response['shipping_address'] = {} #create the dict

        if not (self.cart.address1 and self.cart.city and
              self.cart.state and self.cart.postal_code):
          #we do not have an address stored for this order
          #pull address from WePay and save it as our own

          #US or international address, all should match up except state, postal_code
          if wepay_response.get('shipping_address'):
            self.cart.address_name = wepay_response['shipping_address'].get('name')
            self.cart.address1  = wepay_response['shipping_address'].get('address1')
            self.cart.address2  = wepay_response['shipping_address'].get('address2')
            self.cart.city      = wepay_response['shipping_address'].get('city')
            if wepay_response['shipping_address'].get('country') == 'US':
              self.cart.country = 'USA'
            else:
              self.cart.country = wepay_response['shipping_address'].get('country')

            #check for non-US address first
            if (wepay_response['shipping_address'].get('region') or
                wepay_response['shipping_address'].get('post_code')):
             # international address, all should match except region -> state, post_code -> postal_code
             self.cart.state = wepay_response['shipping_address'].get('region')
             self.cart.postal_code = wepay_response['shipping_address'].get('post_code')

            else: #US address
              self.cart.state = wepay_response['shipping_address'].get('state')
              self.cart.postal_code = wepay_response['shipping_address'].get('zip')
          self.cart.save() #save all our address changes
        return wepay_response

#SIGNALS AND SIGNAL REGISTRATION
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=Checkout)
def createOrders(sender, instance, created, **kwargs):
  checkout = instance
  if (checkout.is_paid and #cart/checkout has been paid for
      checkout.cart.items.count() > 0 and #there are items in the cart
      checkout.orders.count() == 0): #there are no orders yet created

    from apps.public.models.order import Order
    for item in checkout.cart.items.all():
      if item.product.sold_at is not None:
        email = Email(message="customer was just charged for a product someone else already bought")
        email.sendTo([person.email for person in support_team])
      else:
        order = Order(
          checkout            = checkout,
          products_charge     = item.product.price,
          anou_charge         = item.product.anou_fee,
          shipping_charge     = item.product.shipping_cost,
          total_charge        = item.product.intl_price,
          seller_paid_amount  = item.product.price + item.product.shipping_cost
        )
        order.product = item.product
        order.save()
        item.product.sold_at = timezone.now()#todo: make this a post_save order to mark a product sold
        item.product.save()

    # email = Email('checkout/created', checkout)
    # email.assignToOrder(checkout.cart.orders[0])
    # email.sendTo(checkout.cart.email_with_name)

@receiver(post_save, sender=Checkout)
def setPublicId(sender, instance, created, **kwargs):
  if not instance.public_id:
    instance.public_id = "T%d" % instance.pk
    instance.save()

# # Stripe Checkout Data example
#<Charge charge id=ch_14xS5HDICecd6FXNs26nHitv at 0x7ffbdd3d8910> JSON: {
# >>> charge
#   "amount": 42200,
#   "amount_refunded": 0,
#   "balance_transaction": "txn_14xS5HDICecd6FXN2BQ07tLb",
#   "captured": true,
#   "card": {
#     "address_city": null,
#     "address_country": null,
#     "address_line1": null,
#     "address_line1_check": null,
#     "address_line2": null,
#     "address_state": null,
#     "address_zip": null,
#     "address_zip_check": null,
#     "brand": "Visa",
#     "country": "US",
#     "customer": null,
#     "cvc_check": "pass",
#     "dynamic_last4": null,
#     "exp_month": 2,
#     "exp_year": 2018,
#     "fingerprint": "ED4oOCTPx6OnntQC",
#     "funding": "credit",
#     "id": "card_14xRJADICecd6FXNag2jFErT",
#     "last4": "4242",
#     "name": "erstn@stie.com",
#     "object": "card"
#   },
#   "created": 1415664035,
#   "currency": "usd",
#   "customer": null,
#   "description": "hey, it's a charge",
#   "dispute": null,
#   "failure_code": null,
#   "failure_message": null,
#   "fraud_details": {
#     "stripe_report": null,
#     "user_report": null
#   },
#   "id": "ch_14xS5HDICecd6FXNs26nHitv",
#   "invoice": null,
#   "livemode": false,
#   "metadata": {},
#   "object": "charge",
#   "paid": true,
#   "receipt_email": null,
#   "receipt_number": null,
#   "refunded": false,
#   "refunds": {
#     "data": [],
#     "has_more": false,
#     "object": "list",
#     "total_count": 0,
#     "url": "/v1/charges/ch_14xS5HDICecd6FXNs26nHitv/refunds"
#   },
#   "shipping": null,
#   "statement_description": null
# }