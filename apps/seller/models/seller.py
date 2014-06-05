from django.db import models
from apps.admin.models.account import Account
from apps.admin.models.country import Country
from apps.admin.models.currency import Currency
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
  approved_at   = models.DateTimeField(null=True, blank=True) #admin approval #todo: move to store
  deactive_at   = models.DateTimeField(null=True, blank=True) #seller deactivate #todo: move to store

  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  class Meta:
    app_label = 'seller'


  # MODEL PROPERTIES
  @property
  def name(self):
    return self.account.name if self.account.name else ""
  @property
  def email(self):
    return self.account.email if self.account.email else ""
  @property
  def phone(self):
    return self.account.phone if self.account.phone else ""
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


#SIGNALS AND SIGNAL REGISTRATION
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete

@receiver(post_save, sender=Seller)
def updateStore(sender, instance, **kwargs):
  try:
    store = instance.store
    store.save()
  except Exception as e:
    ExceptionHandler(e, "error on seller.updateStore")
