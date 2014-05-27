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
      url_parameters = "?seller_id=%d&destination=%s" % (self.sellers.all()[0].id, reverse('seller:home'))
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
