from django.db import models

from apps.common.models.category import Category
from apps.seller.models.image import Image
from apps.seller.models.seller import Seller


class Asset(models.Model):
  seller        = models.ForeignKey(Seller)
  ilk           = models.CharField(max_length=10)#product,artisan,tool,material
  rank          = models.SmallIntegerField()
  name          = models.CharField(max_length=50, null=True, blank=True)
  description   = models.TextField(null=True, blank=True)
  image         = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL)

  categories    = models.ManyToManyField(Category)

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

  # MODEL PROPERTIES
  # MODEL FUNCTIONS

#SIGNALS AND SIGNAL REGISTRATION
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=Asset)
def createRanking(sender, instance, created, **kwargs):
  if not created:
    products = instance.product_set.all()
    for p in products:
      p.resetSlug()
      p.save() #not necessary, but shows that the save signals will fire
