from django.db import models
from settings.settings import CLOUDINARY

class Seller(models.Model):
  from apps.admin.models import Account, Country, Currency
  account       = models.ForeignKey(Account)#should really be one-to-one relationship
  bio           = models.TextField(null=True, blank=True)
  city          = models.CharField(max_length=50, null=True, blank=True)
  country       = models.ForeignKey(Country, null=True, blank=True)
  coordinates   = models.CharField(max_length=30, null=True, blank=True)
  currency      = models.ForeignKey(Currency, null=True, blank=True)
  image         = models.ForeignKey('Image', null=True, blank=True, on_delete=models.SET_NULL)
  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  @property
  def name(self): return self.account.name if self.account.name else ""
  @property
  def email(self): return self.account.email if self.account.email else ""
  @property
  def phone(self): return self.account.phone if self.account.phone else ""

  def __unicode__(self):
    return self.account.name if self.account.name else "No Name"

class Asset(models.Model):
  from apps.admin.models import Category
  seller        = models.ForeignKey('Seller')
  ilk           = models.CharField(max_length=10)#product,artisan,tool,material
  name          = models.CharField(max_length=50, null=True, blank=True)
  description   = models.TextField(null=True, blank=True)
  image         = models.ForeignKey('Image', null=True, blank=True, on_delete=models.SET_NULL)
  categories    = models.ManyToManyField(Category, null=True, blank=True)
  phone         = models.CharField(max_length=15, null=True, blank=True)

  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return unicode(self.name)

  def get_ilk(self):
    return self._get_ilk_display()

class Product(models.Model):
  from apps.admin.models import Color
  seller        = models.ForeignKey('Seller')

  #product description elements
  assets        = models.ManyToManyField('Asset')
  colors        = models.ManyToManyField(Color)
  width         = models.SmallIntegerField(null=True, blank=True)
  height        = models.SmallIntegerField(null=True, blank=True)
  length        = models.SmallIntegerField(null=True, blank=True)
  weight        = models.SmallIntegerField(null=True, blank=True)
  price         = models.SmallIntegerField(null=True, blank=True)
  shipping_options = models.ManyToManyField('ShippingOption')

  #lifecycle milestones
  active_at     = models.DateTimeField(null=True, blank=True) #seller add
  deactive_at   = models.DateTimeField(null=True, blank=True) #seller remove
  approved_at   = models.DateTimeField(null=True, blank=True) #admin approval
  sold_at       = models.DateTimeField(null=True, blank=True)
  #is_orderable  = models.BooleanField(default=False) #for custom orders

  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  @property
  def was_never_active(self): return True if not self.active_at else False
  #todo: use property.setter functions too!
  #(http://docs.python.org/2/library/functions.html#property)

  @property
  def is_active(self): return True if (self.active_at and not self.deactive_at) else False

  @property
  def is_sold(self): return True if self.sold_at else False

  @property
  def is_approved(self): return True if self.approved_at else False

  @property
  def name(self):
    if len(self.assets.filter(ilk='product')) > 0:
      if self.assets.filter(ilk='product')[0].name:
        return self.assets.filter(ilk='product')[0].name
    return str(self.id)

  @property
  def description(self):
    try: return self.assets.filter(ilk='product')[0].description
    except: return ''

  @property
  def category(self):
    try: return  self.assets.filter(ilk='product')[0].categories.all()[0].name
    except: return ''

  @property
  def rating(self):#overall rating
    from django.db.models import Avg
    #the rounded average of all ratings
    try: return int(round(self.rating_set.aggregate(average=Avg('value'))['average']))
    except: return ''

  @property
  def ratings(self):#rating by subject
    from django.db.models import Avg
    try:
      #get average rating by subject
      query = (self.rating_set.values('subject')
                  .annotate(average=Avg('value'))
                  .values('subject__name','average')
                 )
      #make dictionry: key, value = subject name, rounded rating
      ratings = {}
      for rating in query:
        ratings[rating['subject__name']] = int(round(rating['average']))
      return ratings

    except: return {}

  @property
  def metric_dimensions(self):
    from math import floor
    from django.contrib.gis.measure import Distance
    metric_string = ""
    measurements = sorted([self.width, self.height, self.length], reverse=True)

    for length in measurements:
      if length and Distance(cm=length).m > 1:
        meters = floor(Distance(cm=length).m)
        centimeters = int(round((Distance(cm=length)-Distance(m=meters)).cm))
      elif length:
        meters=None
        centimeters = int(round(Distance(cm=length).cm))
        centimeters = centimeters if centimeters > 0 else 1
      if length:
        dimension_string = ("%dm " % meters) if meters else ""
        dimension_string += "%dcm" % centimeters
        metric_string += "%s x " % dimension_string

    if metric_string.endswith(" x "):
      metric_string = rreplace(metric_string, " x ", "", 1)
    return metric_string

  @property
  def english_dimensions(self):
    from math import floor
    from django.contrib.gis.measure import Distance
    engish_string = ""
    measurements = sorted([self.width, self.height, self.length], reverse=True)

    for length in measurements:
      if length and Distance(cm=length).ft > 1:
        feet = floor(Distance(cm=length).ft)
        inches = int(round((Distance(cm=length) - Distance(ft=feet)).inch))
      elif length:
        feet=None
        inches = int(round(Distance(cm=length).inch))
        inches = inches if inches > 0 else 1
      if length:
        dimension_string = ("%dft " % feet) if feet else ""
        dimension_string += "%din" % inches
        engish_string += "%s x " % dimension_string

    if engish_string.endswith(" x "):
      engish_string = rreplace(engish_string, " x ", "", 1)
    return engish_string

  @property
  def anou_fee(self):
    from settings.settings import ANOU_FEE_RATE
    if self.price:
      fee = self.price * ANOU_FEE_RATE
      return int(round(fee))
    else:
      return 0

  @property
  def shipping_cost(self):
    from apps.seller.controller.shipping import calculateShippingCost
    if self.weight and len(self.shipping_options.all()) > 0:
      return calculateShippingCost(self.weight, self.shipping_options.all()[0])
    else:
      return 0

  @property
  def seller_paid_amount(self):
    if self.price:
      return self.price + self.shipping_cost
    else:
      return 0

  @property
  def local_price(self):
    if self.price:
      return self.price + self.anou_fee + self.shipping_cost
    else:
      return 0

  @property
  def display_price(self, locale='US'):
    cost_amalgum_boobs_bomb = self.local_price
    #convert to USD and round to the nearest $1
    cost_amalgum_boobs_bomb /= self.seller.currency.exchange_rate_to_USD
    cost_amalgum_boobs_bomb = int(round(cost_amalgum_boobs_bomb))
    return cost_amalgum_boobs_bomb

  @property
  def is_complete(self):
    is_product = has_artisan = has_photo = has_price = False
    if len(self.assets.filter(ilk='product')) > 0:
      is_product = True
    if len(self.assets.filter(ilk='artisan')) > 0:
      has_artisan = True
    if len(self.photo_set.all()) > 0:
      has_photo = True
    if self.display_price:
      has_price = True

    if is_product and has_artisan and has_photo and has_price:
      return True
    else:
      return False

  def belongsToPhone(self, phone_number):
    seller_phone = self.seller.account.phone
    return True if (phone_number[-8:] == seller_phone[-8:]) else False

  def __unicode__(self):
    return self.name + ' by ' + self.seller.name

class ShippingOption(models.Model):
  from apps.admin.models import Country
  name          = models.CharField(max_length=50)
  country       = models.ForeignKey(Country)
  #cost_formula  = models.CharField(max_length=50, null=True, blank=True)
  #using varaibles: l,w,h(cm), g=weight(grams)
  image         = models.ForeignKey('Image')

  def __unicode__(self):
    return self.name

class Photo(models.Model): #Photos are exclusively product pictures.
  from settings.settings import MEDIA_URL
  product       = models.ForeignKey(Product)
  rank          = models.SmallIntegerField()
  original      = models.URLField(max_length=200)
  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)\

  def __unicode__(self):
    return unicode(self.original).replace(CLOUDINARY['download_url'],'')

  @property
  def thumb_size(self):
    return u'%s' % self.original.replace("upload", "upload/c_fill,g_center,h_281,q_85,w_375")

  @property
  def pinky_size(self):
    return u'%s' % self.original.replace("upload", "upload/c_fill,g_center,h_75,q_70,w_100")

  @property
  def product_size(self):
    return u'%s' % self.original.replace("upload", "upload/c_pad,h_600,q_70,w_800")

  class Meta:
    unique_together = ('product', 'rank')
    ordering = ['product','rank',]

class Image(models.Model): #Images are used for navigation, thumbnail size
  original      = models.URLField(max_length=200)
  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return unicode(self.original).replace(CLOUDINARY['download_url'],'')

  @property
  def thumb_size(self):
    transformation = "c_fill,g_center,h_225,q_85,w_300"
    return u'%s' % self.original.replace("upload", ("upload/"+transformation))

  @property
  def pinky_size(self):
    transformation = "c_fill,g_center,h_75,q_85,w_100"
    return u'%s' % self.original.replace("upload", ("upload/"+transformation))

def rreplace(s, old, new, occurrence):
  li = s.rsplit(old, occurrence)
  return new.join(li)
