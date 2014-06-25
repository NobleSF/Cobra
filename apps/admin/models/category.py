from django.db import models

class Category(models.Model):
  name            = models.CharField(max_length=50)
  plural_name     = models.CharField(max_length=50)
  keywords        = models.CharField(max_length=50, blank=True, null=True)
  parent_category = models.ForeignKey('self', related_name='sub_categories',
                                      blank=True, null=True)

  ordering_name = models.CharField(max_length=100)

  class Meta:
    ordering = ['ordering_name']
    app_label = 'admin'

  # MODEL PROPERTIES
  @property
  def is_parent_category(self):
    return (not self.parent_category)

  # MODEL FUNCTIONS
  def save(self, *args, **kwargs):
    self.ordering_name = self.get_ordering_name()
    super(Category, self).save(*args, **kwargs)

  def get_ordering_name(self):
    if self.parent_category:
      return u'%s %s' % (unicode(self.parent_category), self.name)
    else:
      return self.name

  def get_absolute_url(self):
    from django.core.urlresolvers import reverse
    return reverse('category', args=[str(self.name)])

  def __unicode__(self):
    return self.name
