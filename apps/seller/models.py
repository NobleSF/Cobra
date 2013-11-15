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
  def title(self):
    return "%s from %s, %s" % (self.name, self.city, self.country.name)

  @property
  def title_description(self):
    try:
      if self.categories_name_string:
        title = "Find %s" % self.categories_name_string
      else:
        title = "Products"
      title += " each uniquly handmade by the artisans of %s" % self.name
      title += " sent to you direct from %s, %s." % (self.city, self.country.name)
      return title
    except:
      return ("Artisans crafts handmade in Morocco." +
              "Our store ships direct from original artisans. " +
              "Made possible by Anou - Beyond Fair Trade.")

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
      if product.parent_category not in categories:
        categories.append(product.parent_category)
    return categories

  @property
  def categories_name_string(self):
    try:
      names_list = [c.name for c in self.categories]
      if len(names_list) > 2:
        return ", and ".join(", ".join(names_list).rsplit(", ",1))
      else:
        return " and ".join(list)
    except:
      return ""

  @property
  def slug(self):
    try:
      from django.template.defaultfilters import slugify
      return slugify(self.title.replace('from ',''))
    except:
      return None

  def get_absolute_url(self):
    from django.core.urlresolvers import reverse
    if self.slug:
      return reverse('store_w_slug', args=[str(self.id), self.slug])
    else:
      return reverse('store', args=[str(self.id)])

  def __unicode__(self):
    return self.name

class Asset(models.Model):
  from apps.admin.models import Category
  seller        = models.ForeignKey('Seller')
  ilk           = models.CharField(max_length=10)#product,artisan,tool,material
  rank          = models.SmallIntegerField()
  name          = models.CharField(max_length=50, null=True, blank=True)
  description   = models.TextField(null=True, blank=True)
  image         = models.ForeignKey('Image', null=True, blank=True, on_delete=models.SET_NULL)
  categories    = models.ManyToManyField(Category, null=True, blank=True)
  phone         = models.CharField(max_length=15, null=True, blank=True)
  #important     = models.BooleanField(default=False)

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
    unique_together = ('seller', 'ilk', 'rank')
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
      if self.assets.filter(ilk='product')[0].name:
        return self.assets.filter(ilk='product')[0].name
      else:
        return str(self.id)
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
      if len(materials) > 2:
        return ", and ".join(", ".join(list).rsplit(", ",1))
      else:
        return " and ".join(list)
    except:
      return ""

  @property
  def tools_name_string(self):
    try:
      list = []
      tools = self.assets.filter(ilk='tool')
      for tool in tools:
        list.append(tool.name)
      if len(tools) > 2:
        #join list with commas, replace last comma with ", and "
        return ", and ".join(", ".join(list).rsplit(", ",1))
      else:
        return " and ".join(list)
    except:
      return ""

  @property
  def title(self): # <=51 chars counting but not using country name
    if (len(self.name) +
        len(self.materials_name_string) +
        len(self.color_adjective) +
        len(self.seller.country.name)) <= 49: #51-2 space chars
      return "%s %s %s" % (self.color_adjective, self.materials_name_string, self.name)
    else:
      return "%s %s" % (self.color_adjective, self.name)

  @property
  def standard_title(self):
    title  = "%s " % self.color_adjective if self.color_adjective else ""
    title += "%s" % self.name
    title += " by %s" % self.seller.name
    title += ", %s" % self.seller.country.name
    return title

  @property
  def title_description(self): # <=160 chars
    try:
      title  = "%s: %s Uniquely handmade by artisans" % (self.category, self.name)
      if self.materials_name_string:
        title += " using %s." % self.materials_name_string
      title += " Crafted by %s" % self.seller.name
      title += " from %s, %s." % (self.seller.city, self.seller.country.name)
      title += " Ships to USA and Europe" if len(title) <= 135 else ""
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
  def parent_category(self):
    try:
      category = self.assets.filter(ilk='product')[0].categories.all()[0]
      if category.is_parent_category:
        return category
      else:
        return category.parent_category
    except:
      return None

  @property
  def category(self):
    try:
      return self.assets.filter(ilk='product')[0].categories.all()[0]
    except:
      return None

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
      fee = self.price * ANOU_FEE_RATE / (1-ANOU_FEE_RATE)
      return int(round(fee)) #round off for local currencies
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
  def usd_price(self): #convert to USD
    if self.local_price:
      local_currency = self.seller.country.currency
      return self.local_price/float(local_currency.exchange_rate_to_USD)
    else:
      return 0

  @property
  def ebay_fee(self): #eBay + PayPal fee is $0.30 plus 12.9% of total
    if self.usd_price:
      fee = 0.30
      fee += (0.129/(1-0.129)) * (self.usd_price + fee)
      return fee
    else:
      return 0

  @property
  def ebay_price(self): #add fees and round to the nearest $1
    if self.usd_price:
      return int(round(self.usd_price + self.ebay_fee))
    else:
      return 0

  @property
  def etsy_fee(self): #Etsy + EtsyCheckout fee is $0.45 plus 6.5% of total
    if self.usd_price:
      fee = 0.40
      fee+= (0.065/(1-0.065)) * (self.usd_price + fee)
      return fee
    else:
      return 0

  @property
  def etsy_price(self): #add fees and round to the nearest $1
    return int(round(self.usd_price + self.etsy_fee))

  @property
  def wepay_fee(self):#wepay fee is $0.30 plus 2.9% of total
    if self.usd_price:
      fee = 0.30
      fee += (0.029/(1-0.029)) * (self.usd_price + fee)
      return fee
    else:
      return 0

  @property
  def display_shipping_price(self, locale='US'):
    return 0

  @property
  def display_price(self): #round to the nearest $1
    return int(round(self.usd_price + self.wepay_fee - self.display_shipping_price))


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
      return slugify(self.title)
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

class Photo(models.Model): #exclusively product photos.
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

class Image(models.Model): #for assets and anything other than product photos
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

  @property
  def peephole(self):
    transformation = "c_fill,g_center,h_75,q_85,w_75,r_max"
    return u'%s' % self.original.replace("upload", ("upload/"+transformation))

  @property
  def headshot(self):
    transformation = "c_fill,w_200,h_200,c_thumb,g_face,r_max"
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
