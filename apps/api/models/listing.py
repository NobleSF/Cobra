from django.db import models
from apps.seller.models.product import Product
from django.utils import timezone
from apps.admin.utils.exception_handling import ExceptionHandler

class ListingManager(models.Manager):
  def for_sale(self):
    return super(ListingManager, self).get_queryset().filter(
            sold_at=None,
            approved_at__lte=timezone.now(),
            active_at__lte=timezone.now(),
            deactive_at=None,
            product__seller__store__approved_at__lte=timezone.now(),
            product__seller__store__deactive_at=None)

  def for_order(self):
    return super(ListingManager, self).get_queryset().filter(
            is_orderable=True,
            approved_at__lte=timezone.now(),
            active_at__lte=timezone.now(),
            deactive_at=None,
            product__seller__store__approved_at__lte=timezone.now(),
            product__seller__store__deactive_at=None)

class Listing(models.Model):
  product             = models.OneToOneField(Product, related_name='listing')

  slug                = models.CharField(max_length=100, null=True, blank=True)
  #title               = models.CharField(max_length=100, null=True, blank=True)
  #standard_title      = models.CharField(max_length=100, null=True, blank=True)
  #title_description   = models.CharField(max_length=300, null=True, blank=True)
  #description         = models.CharField(max_length=1000, null=True, blank=True)
  #price               = models.IntegerField(null=True, blank=True)
  #shipping_price      = models.IntegerField(null=True, blank=True)





  #lifecycle milestones
  active_at           = models.DateTimeField(null=True, blank=True) #seller add
  deactive_at         = models.DateTimeField(null=True, blank=True) #seller remove
  on_hold_at          = models.DateTimeField(null=True, blank=True) #held by admin
  approved_at         = models.DateTimeField(null=True, blank=True) #admin approval
  sold_at             = models.DateTimeField(null=True, blank=True)
  is_orderable        = models.BooleanField(default=False) #for custom orders

  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  # MANAGERS
  objects = ListingManager()

  class Meta:
    app_label = 'api'


  # MODEL PROPERTIES
  @property
  def store(self):
    return self.product.seller.store

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
        message += "<br>%s" % self.product.seller.name
        Email(message=message).sendTo(everyones_emails)
      except Exception as e:
        ExceptionHandler(e, "in Product.is_active")

    #always
    self.on_hold_at = None

  @property
  def was_never_active(self):
    #was never active in it's current state
    #will return true if was active and then deactivated
    return True if not self.active_at else False

  @property
  def is_on_hold(self):
    if self.on_hold_at: return True
    else: return False

  @is_on_hold.setter
  def is_on_hold(self, value):
    if value: #hold
      self.approved_at = None
      self.on_hold_at = timezone.now()
    elif not value: #unhold
      self.on_hold_at = None

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
    self.on_hold_at = None

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
  def materials(self):
    return self.product.assets.filter(ilk='material')

  @property
  def tools(self):
    return self.product.assets.filter(ilk='tool')

  @property
  def utilities(self):
    from itertools import chain
    return list(chain(self.product.materials, self.product.tools))

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
      materials = self.product.assets.filter(ilk='material')
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
      tools = self.product.assets.filter(ilk='tool')
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
    if (len(self.product.name) +
        len(self.materials_name_string) +
        len(self.color_adjective) +
        len(self.product.seller.country.name)) <= 49: #51-2 space chars
      return "%s %s %s" % (self.color_adjective, self.materials_name_string, self.product.name)
    else:
      return "%s %s" % (self.color_adjective, self.product.name)

  @property
  def standard_title(self):
    title  = "%s " % self.color_adjective if self.color_adjective else ""
    title += "%s" % self.product.name
    title += " by %s" % self.product.seller.name
    title += ", %s" % self.product.seller.country.name
    return title

  @property
  def title_description(self): # <=160 chars
    try:
      title  = "%s: %s Uniquely handmade by artisans" % (self.product.category, self.product.name)
      if self.materials_name_string:
        title += " using %s." % self.materials_name_string
      title += " Crafted by %s" % self.product.seller.name
      title += " from %s, %s." % (self.product.seller.city, self.product.seller.country.name)
      title += " Ships to USA and Europe" if len(title) <= 135 else ""
      title += " Qty: 1" if len(title) <= 150 else ""
      return title
    except:
      return ("Artisan craft handmade made in Morocco. Qty: 1 " +
              "For sale on Anou - Moroccan Handmade.")

  @property
  def description(self):
    try: return self.product.assets.filter(ilk='product')[0].description
    except: return ''

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
      local_currency = self.product.seller.country.currency
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
              .filter(seller=self.product.seller)
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
      return unicode("%s %s" % (self.color_adjective, self.product.name))
    else:
      return unicode(self.product.name)


#SIGNALS AND SIGNAL REGISTRATION
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete

@receiver(post_save, sender=Product)
def resetProductPageCache(sender, instance, created, update_fields, **kwargs):
  from apps.public.controllers.events import invalidate_product_cache
  invalidate_product_cache(instance.id)


#SUPPORTING FUNCTIONS
def rreplace(s, old, new, occurrence):
  li = s.rsplit(old, occurrence)
  return new.join(li)
