from django.db import models

class Seller(models.Model):
  from apps.admin.models import Account, Country, Currency
  account       = models.ForeignKey(Account)
  name          = models.CharField(max_length=50)
  email         = models.EmailField(null=True, blank=True)
  phone         = models.BigIntegerField(null=True, blank=True)
  bio           = models.TextField(null=True, blank=True)
  city          = models.CharField(max_length=50, null=True, blank=True)
  country       = models.ForeignKey(Country, null=True, blank=True)
  coordinates   = models.CharField(max_length=30, null=True, blank=True)
  currency      = models.ForeignKey(Currency, null=True, blank=True)
  image         = models.ForeignKey('Image', null=True, blank=True, on_delete=models.SET_NULL)
  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return self.name

class Asset(models.Model):
  from apps.admin.models import Category
  seller        = models.ForeignKey('Seller')
  ilk           = models.CharField(max_length=10)#product,artisan,tool,material
  name          = models.CharField(max_length=50, null=True, blank=True)
  description   = models.TextField(null=True, blank=True)
  image         = models.ForeignKey('Image', null=True, blank=True, on_delete=models.SET_NULL)
  categories    = models.ManyToManyField(Category, null=True, blank=True)
  #phone        = models.CharField(max_length=15, null=True, blank=True)

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
  def is_active(self): return True if self.active_at and not self.deactive_at else False

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
    return unicode(self.original).replace('http://res.cloudinary.com/anou/image/upload/','')

  def _get_thumb_size(self):
    return u'%s' % self.original.replace("upload", "upload/c_pad,h_225,q_85,w_300")
  thumb_size= property(_get_thumb_size)

  def _get_pinky_size(self):
    return u'%s' % self.original.replace("upload", "upload/c_pad,h_75,q_70,w_100")
  pinky_size = property(_get_pinky_size)

  def _get_product_size(self):
    return u'%s' % self.original.replace("upload", "upload/c_pad,h_600,q_70,w_800")
  product_size = property(_get_product_size)

  class Meta:
    ordering = ['product','rank',]

class Image(models.Model): #Images are used for navigation, thumbnail size
  original      = models.URLField(max_length=200)
  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return unicode(self.original).replace('http://res.cloudinary.com/anou/image/upload/','')

  def _get_thumb_size(self):
    return u'%s' % self.original.replace("upload", "upload/c_pad,h_225,q_85,w_300")
  thumb_size = property(_get_thumb_size)

  def _get_pinky_size(self):
    return u'%s' % self.original.replace("upload", "upload/c_pad,h_75,q_70,w_100")
  pinky_size = property(_get_pinky_size)
