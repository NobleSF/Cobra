from django.db import models
from apps.seller.models.product import Product
from settings.settings import CLOUDINARY

class Photo(models.Model): #exclusively product photos.
  from settings.settings import MEDIA_URL
  product         = models.ForeignKey(Product, related_name="photos")
  rank            = models.SmallIntegerField(null=True)
  is_progress     = models.BooleanField(default=False)#of incomplete product or commission
  original        = models.URLField(max_length=200)
  #update history
  created_at      = models.DateTimeField(auto_now_add = True)
  updated_at      = models.DateTimeField(auto_now = True)

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

  # MODEL PROPERTIES
  # MODEL FUNCTIONS
