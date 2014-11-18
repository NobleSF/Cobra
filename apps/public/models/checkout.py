from datetime import timedelta
from django.db import models
from jsonfield import JSONField
from django.utils import timezone
from apps.admin.models import Currency
from apps.admin.utils.exception_handling import ExceptionHandler
from apps.public.models import Cart

class Checkout(models.Model):
  cart                = models.OneToOneField(to=Cart, related_name='checkout')
  public_id           = models.CharField(max_length=15, null=True, blank=True)#todo use pre_save signal, remove null-true

  # id number assigned by the payment provider
  checkout_id         = models.CharField(max_length=35, null=True, blank=True)
  #the data returned by our payment provider
  checkout_data       = JSONField(null=True, blank=True)

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
  def address_name(self): return self.cart.address_name
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
    address  = "%s\n" % (self.address_name or self.name or "")
    address += ("%s\n" % self.address1) if self.address1 else ""
    address += ("%s\n" % self.address2) if self.address2 else ""
    address += ("%s, " % self.city) if self.city else ""
    address += ("%s " % self.state) if self.state else ""
    address += self.postal_code if self.postal_code else ""
    address += ("\n%s" % self.country) if self.country else ""
    return address.upper()


  # MODEL FUNCTIONS
  def clear(self):
    for item in self.cart.item_set.all():
      item.delete()

  def pullStripeData(self):
    #todo: use stripe api to reset our data
    if self.checkout_id.startswith('ch_'):
      return self.checkout_data
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
        if len(product.item_set.all()) > 1:
          for item in product.item_set.all():
            if not item.cart.checked_out:
              item.delete()

    except Exception as e:
      ExceptionHandler(e, "error on cart_class.cleanupCarts")


#SIGNALS AND SIGNAL REGISTRATION

# @receiver(post_save, sender=Checkout)
# def createOrders(sender, instance, created, **kwargs):
#   checkout = instance
#   if (checkout.is_paid and #cart/checkout has been paid for
#       len(checkout.cart.item_set.all()) > 0 and #there are items in the cart
#       len(checkout.orders.all()) == 0): #there are no orders yet created
#     for item in checkout.cart.item_set.all():
#       if item.product.sold_at is not None:
#         email = Email(message="customer was just charged for a product someone else already bought")
#         email.sendTo([person.email for person in support_team])
#       else:
#         order = Order.objects.create(
#           cart                = item.cart,
#           products_charge     = item.product.price,
#           anou_charge         = item.product.anou_fee,
#           shipping_charge     = item.product.shipping_cost,
#           total_charge        = item.product.intl_price,
#           seller_paid_amount  = item.product.price + item.product.shipping_cost
#         )
#         order.save()
#         order.products.add(item.product)
#         item.product.sold_at = timezone.now()
#         item.product.save()

# @receiver(post_save, sender=Checkout)
# def emailCustomer(sender, instance, created, **kwargs):
#   checkout = instance
#   email = Email('checkout/created', checkout)
#   email.assignToOrder(checkout.cart.orders[0])
#   email.sendTo(checkout.cart.email_with_name)