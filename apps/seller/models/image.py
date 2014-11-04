from django.db import models
from settings.settings import CLOUDINARY

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

  # MODEL PROPERTIES
  # MODEL FUNCTIONS
