from django.db import models
from apps.seller.models.product import Product

class Store(models.Model):
  seller              = models.OneToOneField(Seller, related_name='store')

  title         = models.CharField(max_length=100)
  slug          = models.CharField(max_length=100, null=True, blank=True)

  approved_at   = models.DateTimeField(null=True, blank=True) #admin approval
  deactive_at   = models.DateTimeField(null=True, blank=True) #seller deactivate

  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  class Meta:
    app_label = 'api'


  # MODEL PROPERTIES
  @property
  def listings(self):
    from django.utils import timezone
    try:
      listings = (self.seller.products
                      .filter(approved_at__isnull=False,
                              deactive_at=None)
                      .order_by('approved_at').reverse())
      return listings
    except:
      return []

  @property
  def sold_listings(self):
    try:
      listings = (self.products
                      .filter(sold_at__isnull=False,
                              approved_at__isnull=False,
                              deactive_at=None)
                      .order_by('sold_at').reverse())
      return listings
    except:
      return []

  @property
  def description(self):
    try:
      if self.categories_name_string:
        title = "Find %s" % self.seller.categories_name_string
      else:
        title = "Products"
      title += " each uniquly handmade by the artisans of %s " % self.seller.name
      title += "sent to you direct from %s, Morocco." % self.city
      return title
    except:
      return ("Artisans crafts handmade in Morocco." +
              "Our store ships direct from artisan location." +
              "Made possible by Anou - Moroccan Handmade.")

  @property
  def color(self): #todo: make this an editable value only randomly created once
    from apps.admin.utils.color_maker import get_pastel
    if self.id:
      rgb = get_pastel(self.id)
    else:
      rgb = [255,255,255]#white
    return "rgb(%s,%s,%s)" % (rgb[0],rgb[1],rgb[2])

  @property
  def artisans(self):
    return self.seller.artisans

  @property
  def categories(self):
    return self.seller.categories

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


  # MODEL FUNCTIONS
  def get_absolute_url(self):
    from django.core.urlresolvers import reverse
    if not self.slug:
      self.resetSlug()

    try:
      return reverse('store_w_slug', args=[str(self.id), self.slug])
    except:
      return reverse('store', args=[str(self.id)])

  def __unicode__(self):
    return self.title






#SIGNALS AND SIGNAL REGISTRATION
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete

@receiver(pre_save, sender=Store)
def resetTitle(sender, instance, **kwargs):
  try:
    store = instance
    store.title = "%s of %s" % (store.seller.name, store.seller.city)
    store.title = store.title[:85] + ", Morocco"
  except Exception as e:
    ExceptionHandler(e, "error on store.resetTitle")

@receiver(pre_save, sender=Store)
def resetSlug(sender, instance, **kwargs):
  from django.template.defaultfilters import slugify
  try:
    store = instance
    store.slug = slugify("%s of %s" % (store.seller.name, store.seller.city))
    #remove numbers
    store.slug = ''.join([char for char in self.slug if not char.isdigit()])
  except Exception as e:
    ExceptionHandler(e, "error on store.resetSlug")
