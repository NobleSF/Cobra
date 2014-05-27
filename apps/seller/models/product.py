from django.db import models
from apps.admin.models import Color
from apps.seller.models.asset import Asset
from apps.seller.models.seller import Seller
from apps.seller.models.shipping_option import ShippingOption

from django.utils import timezone
from apps.admin.utils.exception_handling import ExceptionHandler

class ProductManager(models.Manager):
  def for_sale(self):
    return super(ProductManager, self).get_queryset().filter(
                                        sold_at=None,
                                        approved_at__lte=timezone.now(),
                                        active_at__lte=timezone.now(),
                                        deactive_at=None,
                                        seller__approved_at__lte=timezone.now(),
                                        seller__deactive_at=None)

class Product(models.Model):
  seller        = models.ForeignKey(Seller)

  #product description elements
  assets        = models.ManyToManyField(Asset)
  colors        = models.ManyToManyField(Color)
  width         = models.SmallIntegerField(null=True, blank=True)
  height        = models.SmallIntegerField(null=True, blank=True)
  length        = models.SmallIntegerField(null=True, blank=True)
  weight        = models.SmallIntegerField(null=True, blank=True)
  price         = models.SmallIntegerField(null=True, blank=True)
  shipping_options = models.ManyToManyField(ShippingOption)

  #lifecycle milestones
  active_at     = models.DateTimeField(null=True, blank=True) #seller add
  deactive_at   = models.DateTimeField(null=True, blank=True) #seller remove
  in_holding    = models.BooleanField(default=False) #held by admin
  #todo: change this to on_hold_at = datetime
  approved_at   = models.DateTimeField(null=True, blank=True) #admin approval
  sold_at       = models.DateTimeField(null=True, blank=True)
  #is_orderable  = models.BooleanField(default=False) #for custom orders

  #dynamically created and updated
  slug          = models.CharField(max_length=150, null=True, blank=True)

  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  #MANAGERS
  objects = ProductManager()

  class Meta:
    ordering = ['-sold_at', '-id']
    app_label = 'seller'

  # MODEL PROPERTIES
  @property
  def is_active(self):
    if self.active_at and not self.deactive_at: return True
    else: return False

  @is_active.setter
  def is_active(self, value):
    from apps.communication.controllers.email_class import Email
    from settings.people import Dan, Brahim, everyones_emails

    if value and self.active_at and not self.deactive_at: #already active
      pass

    elif value: #activate
      self.active_at = timezone.now()
      self.deactive_at = None
      Email('product/activated', self).sendTo([Dan.email, Brahim.email])

    elif not value: #deactivate
      self.deactive_at = timezone.now()
      #cancel orders of this product
      from apps.communication.controllers.order_events import cancelOrder
      for order in self.order_set.all():
        cancelOrder(order)

      try:
        message = "R %d" % self.id
        message += "<br>%s" % self.seller.name
        Email(message=message).sendTo(everyones_emails)
      except Exception as e:
        ExceptionHandler(e, "in Product.is_active")

    #always
    self.in_holding = False

  @property
  def was_never_active(self):
    #was never active in it's current state
    #will return true if was active and then deactivated
    return True if not self.active_at else False

  @property
  def is_on_hold(self):
    if self.in_holding: return True
    else: return False

  @is_on_hold.setter
  def is_on_hold(self, value):
    if value: #hold
      self.approved_at = None
      self.in_holding = True
    elif not value: #unhold
      self.in_holding = False

  @property
  def is_approved(self):
    if self.approved_at and self.is_active: return True
    else: return False

  @is_approved.setter
  def is_approved(self, value):
    if value and self.approved_at: #already approved
      pass
    elif value: #approve
      self.approved_at = timezone.now()
      self.resetSlug()
    elif not value: #unapprove or disapprove #todo: separate these actions
      self.approved_at = None
    #always:
    self.in_holding = False

  @property
  def is_sold(self):
    if self.sold_at: return True
    else: return False

  @is_sold.setter
  def is_sold(self, value):
    if value and self.sold_at: #already sold
      pass
    elif value:
      self.sold_at = timezone.now()
    elif not value:
      self.sold_at = None

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
  def photo(self):
    try:
      return self.photos.exclude(is_progress=True)[0]
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
  def artisan(self):
    try:
      return self.assets.filter(ilk='artisan')[0]
    except:
      return None

  @property
  def materials(self):
    return self.assets.filter(ilk='material')

  @property
  def tools(self):
    return self.assets.filter(ilk='tool')

  @property
  def utilities(self):
    from itertools import chain
    return list(chain(self.materials, self.tools))

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
      return self.category if self.category.is_parent_category else self.category.parent_category
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
  def longest_side_english(self):#todo: clean this up
    longest = sorted([self.width, self.height, self.length], reverse=True)[0]
    inches = int(round(longest/2.54))
    if inches > 18:
      feet = int(inches / 12)
      inches = inches % 12
    else:
      feet = 0
      inches = inches if inches > 0 else 1
    dimension_string = ("%dft " % feet) if feet else ""
    dimension_string += ("%din" % inches) if inches else ""
    return dimension_string

  @property
  def second_longest_side_english(self):#todo clean this up
    longest = sorted([self.width, self.height, self.length], reverse=True)[1]
    inches = int(round(longest/2.54))
    if inches > 18:
      feet = int(inches / 12)
      inches = inches % 12
    else:
      feet = 0
      inches = inches if inches > 0 else 1
    dimension_string = ("%dft " % feet) if feet else ""
    dimension_string += ("%din" % inches) if inches else ""
    return dimension_string

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
    from apps.seller.controllers.shipping import calculateShippingCost
    if self.weight and len(self.shipping_options.all()) > 0:
      return calculateShippingCost(self.weight, self.shipping_options.all()[0], 'US')
    else:
      return 0

  @property
  def local_shipping_cost(self):
    from apps.seller.controllers.shipping import calculateShippingCost
    if self.weight and len(self.shipping_options.all()) > 0:
      return calculateShippingCost(self.weight, self.shipping_options.all()[0], 'MA')
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
      return self.price + self.anou_fee + self.local_shipping_cost
    else:
      return 0

  @property
  def intl_price(self):
    if self.price:
      return self.price + self.anou_fee + self.shipping_cost
    else:
      return 0

  @property
  def usd_price(self): #convert to USD
    if self.intl_price:
      local_currency = self.seller.country.currency
      return self.intl_price/float(local_currency.exchange_rate_to_USD)
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
      fee += (0.065/(1-0.065)) * (self.usd_price + fee)
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
    if (self.assets.filter(ilk='product').count() #has product type
        and self.assets.filter(ilk='artisan').count() #has artisan
        and self.photos.count() #has photo
        and self.shipping_options.count() #has shipping option
        and self.display_price #has price
        and self.weight #has weight
    ):
      return True
    else:
      return False

  @property
  def pinterest_url(self):
    try:
      return ("http://www.pinterest.com/pin/create/button/" +
              "?url=http://www.theanou.com" + self.get_absolute_url() +
              "&media=" + self.photo.original +
              "&description=" + self.title_description)
    except:
      return "" #probably doesn't need to be working anyway

  # MODEL FUNCTIONS
  def get_related_products(self, limit=3):
    from django.utils import timezone
    try:
      return (Product.objects.for_sale()
              .filter(seller=self.seller)
              .exclude(id=self.id))[:limit]
      #todo: create recommendation engine
    except:
      return []

  def resetSlug(self):
    from django.template.defaultfilters import slugify
    try:
      self.slug = slugify(self.title)
      self.slug = ''.join([char for char in self.slug if not char.isdigit()])
      self.save()
    except: pass

  def belongsToPhone(self, phone_number):
    try:
      seller_phone = self.seller.account.phone
      return True if (phone_number[-8:] == seller_phone[-8:]) else False
    except Exception as e:
      ExceptionHandler(e, "in Product.belongsToPhone")
      return False

  def get_absolute_url(self):
    from django.core.urlresolvers import reverse
    if not self.slug:
      self.resetSlug()

    try:
      return reverse('product_w_slug', args=[str(self.id), self.slug])
    except:
      return reverse('product', args=[str(self.id)])

  def __unicode__(self):
    if self.color_adjective:
      return unicode("%s %s" % (self.color_adjective, self.name))
    else:
      return unicode(self.name)

#SUPPORTING FUNCTIONS
def rreplace(s, old, new, occurrence):
  li = s.rsplit(old, occurrence)
  return new.join(li)

#SIGNALS AND SIGNAL REGISTRATION
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete

@receiver(pre_delete, sender=Product)
def onDelete(sender, instance, **kwargs):
  try:
    #todo: copy instance to reporting app
    instance.assets.clear()
    instance.colors.clear()
    instance.shipping_options.clear()
  except Exception as e:
    ExceptionHandler(e, "error on product.onDelete pre_delete signal")

@receiver(post_save, sender=Product)
def createRanking(sender, instance, created, update_fields, **kwargs):
  try:
    from apps.public.models import Ranking
    from apps.public.controllers.product_ranking import updateRankings, newProductResult
    if created:
      ranking, is_new = Ranking.objects.get_or_create(product = instance)
      ranking.new_product = newProductResult(instance)
  except Exception as e:
    ExceptionHandler(e, "error on product.createRanking post_save signal")

@receiver(post_save, sender=Product)
def resetProductPageCache(sender, instance, created, update_fields, **kwargs):
  from apps.public.controllers.events import invalidate_product_cache
  invalidate_product_cache(instance.id)
