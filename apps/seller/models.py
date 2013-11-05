from django.db import models
from settings.settings import CLOUDINARY

class Seller(models.Model):
  from apps.admin.models import Account, Country, Currency
  account       = models.ForeignKey(Account, related_name='sellers')#should really be one-to-one relationship
  bio           = models.TextField(null=True, blank=True)
  city          = models.CharField(max_length=50, null=True, blank=True)
  country       = models.ForeignKey(Country, null=True, blank=True)
  coordinates   = models.CharField(max_length=30, null=True, blank=True)
  image         = models.ForeignKey('Image', null=True, blank=True, on_delete=models.SET_NULL)

  #Original Language
  #name_ol       = models.CharField(max_length=50, null=True, blank=True)
  bio_ol = models.TextField(null=True, blank=True)

  #account lifecycle
  translated_by = models.ForeignKey(Account, null=True, blank=True, related_name='translator')
  approved_at   = models.DateTimeField(null=True, blank=True) #admin approval
  deactive_at   = models.DateTimeField(null=True, blank=True) #seller deactivate

  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  @property
  def title(self): return "%s from %s, %s" % (self.name, self.city, self.country.name)

  @property
  def name(self): return self.account.name if self.account.name else ""
  @property
  def username(self): return self.account.username
  @property
  def email(self): return self.account.email if self.account.email else ""
  @property
  def phone(self): return self.account.phone if self.account.phone else ""

  @property
  def bank_name(self):
    return self.account.bank_name if self.account.bank_name else ""
  @property
  def bank_account(self):
    return self.account.bank_account if self.account.bank_account else ""

  @property
  def categories(self):
    from django.utils import timezone
    products = self.product_set.filter(approved_at__lte=timezone.now())
    categories = []
    for product in products:
      if product.category not in categories:
        categories.append(product.category)
    return categories

  def __unicode__(self):
    return self.name

  def get_absolute_url(self):
    from django.core.urlresolvers import reverse
    return reverse('store', args=[str(self.id)])

class Asset(models.Model):
  from apps.admin.models import Category
  seller        = models.ForeignKey('Seller')
  ilk           = models.CharField(max_length=10)#product,artisan,tool,material
  rank          = models.SmallIntegerField(null=True, blank=True)
  #todo: give all assets ranks and remove "nullable"
  name          = models.CharField(max_length=50, null=True, blank=True)
  description   = models.TextField(null=True, blank=True)
  image         = models.ForeignKey('Image', null=True, blank=True, on_delete=models.SET_NULL)
  categories    = models.ManyToManyField(Category, null=True, blank=True)
  phone         = models.CharField(max_length=15, null=True, blank=True)

  #Original Language
  name_ol       = models.CharField(max_length=50, null=True, blank=True)
  description_ol = models.TextField(null=True, blank=True)

  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return unicode(self.name)

  @property
  def title(self):
    return "%s from %s, %s" % (self.name, self.seller.city, self.seller.country.name)

  def get_ilk(self):
    return self._get_ilk_display()

  class Meta:
    #unique_together = ('seller', 'ilk', 'rank')
    #todo: turn on once rank not nullable
    ordering = ['rank', 'created_at']

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
  in_holding    = models.BooleanField(default=False) #unable to be approved
  approved_at   = models.DateTimeField(null=True, blank=True) #admin approval
  sold_at       = models.DateTimeField(null=True, blank=True)
  #is_orderable  = models.BooleanField(default=False) #for custom orders
  #is_hidden     = being sold on another platform (etys, ebay)

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
  def is_recently_sold(self):
    from django.utils import timezone
    from datetime import timedelta
    if self.sold_at:
      one_day = timedelta(days=1)
      time_since_sold = timezone.now() - self.sold_at
      if self.sold_at and one_day > time_since_sold:
        return True
      else:
        return False
    else:
      return False

  @property
  def is_approved(self): return True if (self.approved_at and self.is_active) else False

  @property
  def photo(self):
    try:
      return self.photos.all()[0]
    except:
      return None

  @property
  def name(self):
    try:
      return self.assets.filter(ilk='product')[0].name
    except:
      return str(self.id)

  @property
  def color_adjective(self): #5-15 chars
    try:
      colors = self.colors.all()
      if colors.count() == 1:
        return "%s" % colors[0].name
      elif colors.count() <= 3:
        return "%s, %s" % (colors[0].name, colors[1].name)
      elif colors.count() > 3:
        return "Colored"
      else:
        return ""
    except:
      return ""

  @property
  def materials_name_string(self):
    try:
      list = []
      materials = self.assets.filter(ilk='material')
      for material in materials:
        list.append(material.name)
      return ", and".join(", ".join(list).rsplit(",",1))
    except:
      return None

  @property
  def tools_name_string(self):
    try:
      list = []
      tools = self.assets.filter(ilk='tool')
      for tool in tools:
        list.append(tool.name)
      #join list with commas, replace last comma with ", and "
      return ", and".join(", ".join(list).rsplit(",",1))
    except:
      return None

  @property
  def short_title(self): # <40 chars
    return "%s %s" % (self.color_adjective, self.name)

  @property
  def title(self):
    title  = "%s " % self.color_adjective if self.color_adjective else ""
    title += "%s" % self.name
    title += " by %s" % self.seller.name
    title += ", %s" % self.seller.country.name
    return title

  @property
  def long_title(self): # <160 chars
    try:
      title  = "%s by %s: This " % (self.category, self.seller.name)
      title += "%s " % self.color_adjective if self.color_adjective else ""
      title += "%s is uniquely handmade" % self.name
      title += " by artisans from %s, %s" % (self.seller.city, self.seller.country.name)
      if self.materials_name_string:
        title += " with %s" % self.materials_name_string
      if self.tools_name_string and (len(title) + len(self.tools_name_string)) < 160:
        title += " using %s" % self.tools_name_string
      title += "."
      title += " Qty: 1" if len(title) <= 150 else ""
      return title
    except:
      return ("Artisan craft handmade made in Morocco. Qty: 1 " +
              "For sale on Anou - Beyond Fair Trade.")

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
    metric_string = ""
    measurements = sorted([self.width, self.height, self.length], reverse=True)

    for length in measurements:
      if length:
        centimeters = int(round(length))
        if centimeters >= 100:
          meters = int(round(centimeters / 100))
          centimeters = centimeters % 100
        else:
          meters = 0
          centimeters = centimeters if centimeters > 0 else 1
        dimension_string = ("%dm " % meters) if meters else ""
        dimension_string += "%dcm" % centimeters if centimeters else ""
        metric_string += "%s x " % dimension_string

    if metric_string.endswith(" x "):
      metric_string = rreplace(metric_string, " x ", "", 1)
    return metric_string

  @property
  def english_dimensions(self):
    engish_string = ""
    measurements = sorted([self.width, self.height, self.length], reverse=True)

    for length in measurements:
      if length:
        inches = int(round(length/2.54))
        if inches > 18:
          feet = int(inches / 12)
          inches = inches % 12
        else:
          feet = 0
          inches = inches if inches > 0 else 1
        dimension_string = ("%dft " % feet) if feet else ""
        dimension_string += ("%din" % inches) if inches else ""
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
    cost_amalgum_boobs_bomb /= self.seller.country.currency.exchange_rate_to_USD
    cost_amalgum_boobs_bomb = int(round(cost_amalgum_boobs_bomb))
    return cost_amalgum_boobs_bomb

  @property
  def display_shipping_price(self, locale='US'):
    return 0

  @property
  def is_complete(self):
    if (self.assets.filter(ilk='product').count() and #has product type
        self.assets.filter(ilk='artisan').count() and #has artisan
        self.photos.count() and #has photo
        self.display_price #has price
    ):
      return True
    else:
      return False

  def belongsToPhone(self, phone_number):
    if self.seller.account.phone:
      seller_phone = self.seller.account.phone
      return True if (phone_number[-8:] == seller_phone[-8:]) else False
    else: return False

  @property
  def slug(self):
    try:
      from django.template.defaultfilters import slugify
      return slugify(self.short_title)
    except:
      return None

  def get_absolute_url(self):
    from django.core.urlresolvers import reverse
    if self.slug:
      return reverse('product_w_slug', args=[str(self.id), self.slug])
    else:
      return reverse('product', args=[str(self.id)])

  def __unicode__(self):
    if self.color_adjective:
      return "%s%s" % (self.color_adjective, self.name)
    else:
      return self.name

  class Meta:
    ordering = ['-sold_at', '-id']

class ShippingOption(models.Model):
  from apps.admin.models import Country
  name          = models.CharField(max_length=50)
  country       = models.ForeignKey(Country)
  image         = models.ForeignKey('Image', null=True, blank=True, on_delete=models.SET_NULL)

  def __unicode__(self):
    return self.name

class Photo(models.Model): #Photos are exclusively product pictures.
  from settings.settings import MEDIA_URL
  product       = models.ForeignKey(Product, related_name="photos")
  rank          = models.SmallIntegerField()
  original      = models.URLField(max_length=200)
  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

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

class Upload(models.Model): #images and photos before they exist
  public_id     = models.CharField(max_length=100, unique=True)
  created_at    = models.DateTimeField(auto_now_add = True)
  complete_at   = models.DateTimeField(null=True, blank=True)
  url           = models.URLField(max_length=200, null=True, blank=True)

  @property
  def is_complete(self): return True if self.complete_at else False

def rreplace(s, old, new, occurrence):
  li = s.rsplit(old, occurrence)
  return new.join(li)
