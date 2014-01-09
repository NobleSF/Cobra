from django.db import models

class Account(models.Model):
  username      = models.CharField(max_length=50, blank=True, null=True, unique=True)
  password      = models.CharField(max_length=64)
  name          = models.CharField(max_length=50, blank=True, null=True)
  email         = models.EmailField(blank=True, null=True, unique=True)
  phone         = models.CharField(max_length=15, blank=True, null=True, unique=True)
  bank_name     = models.CharField(max_length=50, blank=True, null=True)
  bank_account  = models.CharField(max_length=100, blank=True, null=True)

  admin_type    = models.CharField(max_length=20, null=True)#super,country,trainer,translator
                  #todo: create priveledges table with country assignments

  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  @property
  def is_admin(self): return True if self.admin_type else False

  @property
  def cheat_login_url(self):
    from django.core.urlresolvers import reverse
    try:
      url = reverse('admin:login cheat')
      url_parameters = "?seller_id=%d&destination=%s" % (self.sellers.all()[0].id, reverse('seller:management home'))
    except:
      return reverse('login')
    else:
      return url + url_parameters

  @property
  def seller(self):
    try: return self.sellers.all()[0]
    except: return None

  def __unicode__(self):
    return self.username

class Country(models.Model): #could expand on pypi.python.org/pypi/django-countries
  name          = models.CharField(max_length=100)
  code          = models.CharField(max_length=3)
  calling_code  = models.IntegerField()
  # assuming countries stick to one currency nationwide
  currency      = models.ForeignKey('Currency')

  def __unicode__(self):
    return self.code

class Currency(models.Model):
  name          = models.CharField(max_length=50)
  code          = models.CharField(max_length=3)
  exchange_rate_to_USD = models.FloatField(verbose_name='Exchange Rate')
  updated_at    = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return self.code

class Color(models.Model):
  name          = models.CharField(max_length=15)
  hex_value     = models.CharField(max_length=6)

  def __unicode__(self):
    return self.name

  class Meta:
    ordering = ['id']

class Category(models.Model):
  name          = models.CharField(max_length=50)
  plural_name   = models.CharField(max_length=50)
  keywords      = models.CharField(max_length=50, blank=True, null=True)
  parent_category = models.ForeignKey('self', related_name='sub_categories',
                                      blank=True, null=True)

  ordering_name = models.CharField(max_length=100)

  @property
  def is_parent_category(self):
    return (not self.parent_category)

  def save(self, *args, **kwargs):
    self.ordering_name = self.get_ordering_name()
    super(Category, self).save(*args, **kwargs)

  def get_ordering_name(self):
    if self.parent_category:
      return u'%s %s' % (unicode(self.parent_category), self.name)
    else:
      return self.name

  def __unicode__(self):
    return self.name

  class Meta:
    ordering = ['ordering_name']

class RatingSubject(models.Model):
  #we may be able to move this to a list of choices for the Rating model
  name          = models.CharField(max_length=20)

  def __unicode__(self):
    return self.name
