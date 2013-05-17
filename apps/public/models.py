from django.db import models

class Cart(models.Model):
  email               = models.EmailField(blank=True, null=True, unique=True)
  name                = models.CharField(max_length=100, null=True, blank=True)
  address1            = models.CharField(max_length=100, null=True, blank=True)
  address2            = models.CharField(max_length=100, null=True, blank=True)
  city                = models.CharField(max_length=50,  null=True, blank=True)
  state               = models.CharField(max_length=50,  null=True, blank=True)
  postal_code         = models.CharField(max_length=15,  null=True, blank=True)
  country             = models.CharField(max_length=50,  null=True, blank=True)

  checked_out         = models.BooleanField(default=False)

  #update history
  created_at          = models.DateTimeField(auto_now_add = True)
  updated_at          = models.DateTimeField(auto_now = True)

  def discount(self):
    #for when we implement shipping groups and discounts
    return 0

  def total(self):
    sum = 0
    for item in self.items:
      sum += item.price
    return sum

class Item(models.Model):
  from apps.seller.models import Product

  cart                = models.ForeignKey('Cart')
  product             = models.ForeignKey(Product)
  #quantity           = models.PositiveIntegerField(default=1)

  def __unicode__(self):
    #return u'%d units of %s' % (self.quantity, self.product.__name__)
    return self.product.name

  def price(self):
    return self.product.display_price

  def photos(self):
    from apps.seller.models import Photo
    return Photo.objects.filter(product_id=self.product.id)

  def photo(self):
    photos = self.photos()
    return photos[0]

class Order(models.Model):
  from apps.seller.models import Product, ShippingOption
  from apps.admin.models import Account
  account             = models.ForeignKey(Account)#what if no customer accounts?
  notes               = models.TextField(blank=True, null=True)

  #charges breakdown
  products_charge     = models.DecimalField(max_digits=6, decimal_places=2)
  shipping_charge     = models.DecimalField(max_digits=6, decimal_places=2)
  anou_charge         = models.DecimalField(max_digits=6, decimal_places=2)
  discount_charge     = models.DecimalField(max_digits=6, decimal_places=2)
  discount_reason     = models.TextField(blank=True, null=True)
  total_charge        = models.DecimalField(max_digits=6, decimal_places=2)
  receipt             = models.TextField(blank=True, null=True)

  #cart                = models.ForiegnKey('Cart')
  shipping_option     = models.ForeignKey(ShippingOption)
  #reported weight and cost after shipped
  shipping_weight     = models.FloatField(blank=True, null=True)
  shipping_cost       = models.DecimalField(blank=True, null=True,
                                            max_digits=6, decimal_places=2)
  shipped_date        = models.DateField(blank=True, null=True)
  received_date       = models.DateField(blank=True, null=True)

  #order items
  products            = models.ManyToManyField(Product)

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
  from apps.seller.models import Product
  from apps.admin.models import Account, RatingSubject
  account             = models.ForeignKey(Account)
  product_id          = models.ForeignKey(Product)
  subject             = models.ForeignKey(RatingSubject)
  value               = models.SmallIntegerField()
  created_at          = models.DateTimeField(auto_now_add = True)

  def __unicode__(self):
    return self.value

class CustomerActivity(models.Model):
  from apps.seller.models import Product
  # ip address?
  # account_id?
  product_id          = models.ForeignKey(Product) # is this neccessary?
  action              = models.CharField(max_length=10) #what are the options?
  value               = models.IntegerField() #what's this for?
  created_at          = models.DateTimeField(auto_now_add = True)

class Visitor(models.Model):
  from django.contrib.sessions.models import Session

  sessions            = models.ManyToManyField(Session)
  carts               = models.ForeignKey('Cart', null=True, blank=True)
