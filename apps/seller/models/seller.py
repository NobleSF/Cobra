from django.db import models
from apps.admin.models.account import Account
from apps.admin.models.country import Country

from apps.seller.models.image import Image

class Seller(models.Model):
  account       = models.ForeignKey(Account, related_name='sellers')
                #should really be one-to-one relationship
  bio           = models.TextField(null=True, blank=True)
  city          = models.CharField(max_length=50, null=True, blank=True)
  country       = models.ForeignKey(Country, null=True, blank=True)
  coordinates   = models.CharField(max_length=30, null=True, blank=True)
  image         = models.ForeignKey(Image, null=True, blank=True,
                                    on_delete=models.SET_NULL)

  #Original Language
  #name_ol       = models.CharField(max_length=50, null=True, blank=True)
  bio_ol = models.TextField(null=True, blank=True)

  #account lifecycle
  translated_by = models.ForeignKey(Account, null=True, blank=True,
                                    related_name='translator')
  approved_at   = models.DateTimeField(null=True, blank=True) #admin approval
  deactive_at   = models.DateTimeField(null=True, blank=True) #seller deactivate

  slug          = models.CharField(max_length=150, null=True, blank=True)

  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  class Meta:
    app_label = 'seller'

  # MODEL PROPERTIES
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
      title += " each uniquly handmade by the artisans of %s " % self.name
      title += "sent to you direct from %s, %s." % (self.city, self.country.name)
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
  def artisans(self):
    try:
      return self.asset_set.filter(ilk='artisan')
    except:
      return None

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

  # MODEL FUNCTIONS
  def get_store_products(self, limit=None):
    from django.utils import timezone
    try:
      products = (self.product_set
                      .filter(sold_at=None,
                              approved_at__lte=timezone.now(),
                              deactive_at=None)
                      .order_by('approved_at').reverse())[:limit]
      return products
    except:
      return []

  def get_sold_products(self, limit=None):
    from django.utils import timezone
    try:
      products = (self.product_set
                      .filter(sold_at__lte=timezone.now(),
                              approved_at__lte=timezone.now(),
                              deactive_at=None)
                      .order_by('sold_at').reverse())[:limit]
      return products
    except:
      return []

  def resetSlug(self):
    from django.template.defaultfilters import slugify
    try:
      self.slug = slugify(self.title.replace('from ',''))
      self.slug = ''.join([char for char in self.slug if not char.isdigit()])
      self.save()
    except: pass

  def get_absolute_url(self):
    from django.core.urlresolvers import reverse
    if not self.slug:
      self.resetSlug()

    try:
      return reverse('store_w_slug', args=[str(self.id), self.slug])
    except:
      return reverse('store', args=[str(self.id)])

  def __unicode__(self):
    return self.name
