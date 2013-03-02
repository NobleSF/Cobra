from django.db import models

class Order(models.Model):
  from seller.models import Product, ShippingOption
  from admin.models import Account
  account             = models.ForeignKey(Account)
  notes               = models.TextField(blank=True, null=True)
  #charges breakdown
  products_charge     = models.DecimalField(max_digits=6, decimal_places=2)
  shipping_charge     = models.DecimalField(max_digits=6, decimal_places=2)
  anou_charge         = models.DecimalField(max_digits=6, decimal_places=2)
  discount_charge     = models.DecimalField(max_digits=6, decimal_places=2)
  discount_reason     = models.TextField(blank=True, null=True)
  total_charge        = models.DecimalField(max_digits=6, decimal_places=2)
  receipt             = models.TextField(blank=True, null=True)
  #shipping info
  shipped_on          = models.DateField(blank=True, null=True)
  shipping_address    = models.TextField()
  shipping_option     = models.ForeignKey(ShippingOption)
  shipping_weight     = models.FloatField(blank=True, null=True)
  shipping_cost       = models.DecimalField(blank=True, null=True,
                                            max_digits=6, decimal_places=2)
  received_on         = models.DateField(blank=True, null=True)
  #order items
  product             = models.ManyToManyField(Product)
  #Status
  is_seller_notified  = models.BooleanField(default=False)
  is_seller_confirmed = models.BooleanField(default=False)
  is_shipped          = models.BooleanField(default=False)
  is_arrived          = models.BooleanField(default=False)
  is_reviewed         = models.BooleanField(default=False)
  is_artisan_paid     = models.BooleanField(default=False)
  #update history
  created_at          = models.DateTimeField(auto_now_add = True)
  updated_at          = models.DateTimeField(auto_now = True)

class Rating(models.Model):
  from seller.models import Product
  from admin.models import Account, RatingSubject
  account             = models.ForeignKey(Account)
  product_id          = models.ForeignKey(Product)
  subject             = models.ForeignKey(RatingSubject)
  value               = models.SmallIntegerField()
  created_at          = models.DateTimeField(auto_now_add = True)

  def __unicode__(self):
    return self.value

class CustomerActivity(models.Model):
  from seller.models import Product
  # ip address?
  # account_id?
  product_id          = models.ForeignKey(Product) # is this neccessary?
  action              = models.CharField(max_length=10) #what are the options?
  value               = models.IntegerField() #what's this for?
  created_at          = models.DateTimeField(auto_now_add = True)
