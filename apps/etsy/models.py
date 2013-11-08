from django.db import models
from django.utils import timezone
from apps.seller.models import Seller, Product, Image

class Shop(models.Model):
  seller            = models.OneToOneField(Seller, related_name='etsy_shop')

  user_id           = models.CharField(max_length=10)
  login_name        = models.CharField(max_length=50)
  auth_token        = models.TextField(null=True, blank=True)
  auth_token_secret = models.TextField(null=True, blank=True)

  shop_id           = models.BigIntegerField()
  shop_name         = models.CharField(max_length=50)
  title             = models.CharField(max_length=50, null=True, blank=True)
  banner_image      = models.ForeignKey(Image, null=True, blank=True,
                                        on_delete=models.SET_NULL)

  #Etsy update history
  synced_at         = models.DateTimeField(null=True, blank=True)

  #update history
  created_at        = models.DateTimeField(auto_now_add = True)
  updated_at        = models.DateTimeField(auto_now = True)

  @property
  def is_authorized(self):
    return True if (self.auth_token and self.auth_token_secret) else False

  @property
  def user_email(self):
    return 'etsy_shop+%s@theanou.com' % self.shop_name

  @property
  def user_image(self):
    try:
      return self.seller.assets.filter(ilk='artisan')[0].image
    except: return None

  @property
  def default_title(self): return self.seller.title
  @property
  def announcement(self): return "Find {category list}"
  @property
  def sale_message(self): return "You just bought a thing, nice job."
  @property
  def policy_welcome(self): return "Our policy is to welcome you."
  @property
  def policy_shipping(self): return "Our policy is to send you what you paid for."
  @property
  def policy_refunds(self): return "Our policy is to refund what is broken or lost."
  @property
  def policy_seller_info(self): return "Our policy is to tell you about us."
  @property
  def policy_additional(self): return "Our policy to not stop until we go too far."

  @property
  def is_vacation(self): return self.seller.is_deactive
  @property
  def vacation_message(self): return "We are temporarily closed for business."

  @property
  def currency_code(self): return "USD"
  @property
  def ga_code(self): return "" #google analytics code


class Listing(models.Model):
  product           = models.OneToOneField(Product, related_name='etsy_listing')
  listing_id        = models.BigIntegerField(null=True, blank=True)

  #active, removed, sold_out, expired, etc...

  shop              = models.ForeignKey(Shop)
  shop_section_id   = models.IntegerField(null=True, blank=True)
  category_id       = models.IntegerField(null=True, blank=True)#listing category

  listed_price      = models.DecimalField(max_digits=6, decimal_places=2,
                                          null=True, blank=True)
  listed_shipping   = models.DecimalField(max_digits=6, decimal_places=2,
                                          null=True, blank=True)

  #Etsy update history
  listed_at         = models.DateTimeField(null=True, blank=True)
  unlisted_at       = models.DateTimeField(null=True, blank=True)
  synced_at         = models.DateTimeField(null=True, blank=True)
  sold_at           = models.DateTimeField(null=True, blank=True)
  #unlisted_at

  #update history
  created_at        = models.DateTimeField(auto_now_add = True)
  updated_at        = models.DateTimeField(auto_now = True)

  @property
  def title(self): return self.product.long_title
  @property
  def description(self): return self.product.description
  @property
  def price(self): return self.product.etsy_price

  @property
  def state(self):
    if   self.sold_at:      return 'sold_out'
    elif self.unlisted_at:  return 'inactive'
    elif self.listed_at:    return 'active'
    else:                   return 'draft'

  @property
  def tags(self):
    try:
      keyword_string = self.product.category.keywords
      #split on commas and spaces, create list, remove empty values
      return filter(bool, keyword_string.replace(',',' ').split(' '))
    except:
      return []

  @property
  def materials(self):
    materials = []
    try:
      for material in self.product.assets.filter(ilk='material'):
        materials.append(material.name)
      return materials
    except: pass
    return materials

  @property
  def user_id(self): return self.shop.user_id
  @property
  def currency_code(self): return self.shop.currency_code
  @property
  def quantity(self): return 1
  @property
  def processing_min(self): return 2 #2 days
  @property
  def processing_max(self): return 5 #5 days

  @property
  def who_made(self): return "collective" #i_did, someone_else
  @property
  def is_supply(self): return False
  @property
  def when_made(self): return "2010_2013"
  @property
  def is_private(self): return False
  @property
  def recipient(self): return "unisex_adults"
  #@property
  #def occasion(self): return ""
  @property
  def style(self): return ['handmade','fair-trade']
  @property
  def is_customizable(self): return False
  #@property
  #def is_digital(self): return False

class Transaction(models.Model):
  from apps.public.models import Order

  transaction_id    = models.BigIntegerField()
  shop              = models.ForeignKey(Shop)
  listing           = models.ForeignKey(Listing)
  order             = models.ForeignKey(Order)

  receipt_id        = models.BigIntegerField()

  paid_at           = models.DateTimeField()

  price_paid        = models.DecimalField(max_digits=8, decimal_places=2,
                                          null=True, blank=True)
  currency          = models.CharField(max_length=5, null=True, blank=True)

  #update history
  created_at        = models.DateTimeField(auto_now_add = True)
  updated_at        = models.DateTimeField(auto_now = True)

  @property
  def shipped_at(self):
    if self.order:
      return self.order.shipped_at
    else:
      return None
