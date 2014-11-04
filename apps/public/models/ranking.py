from django.db import models
from apps.seller.models.product import Product

class Ranking(models.Model):
  product       = models.OneToOneField(Product)
  photography   = models.DecimalField(max_digits=3, decimal_places=2, default='0.50')
  price         = models.DecimalField(max_digits=3, decimal_places=2, default='0.50')
  appeal        = models.DecimalField(max_digits=3, decimal_places=2, default='0.50')
  new_product   = models.DecimalField(max_digits=3, decimal_places=2, default='1.00')
  new_store     = models.DecimalField(max_digits=3, decimal_places=2, default='1.00')

  #update history
  updated_at    = models.DateTimeField(auto_now = True)

  # MODEL PROPERTIES
  @property
  def subjects(self):
    return {'photography':  self.photography,
            'price':        self.price,
            'appeal':       self.appeal,
            'new_product':  self.new_product,
            'new_store':    self.new_store
           }

  @property
  def weighted_average(self):
    from apps.public.controller.product_ranking import WEIGHTS
    avg  = 0.0
    avg += float(self.photography * WEIGHTS['photography'])
    avg += float(self.price       * WEIGHTS['price'])
    avg += float(self.appeal      * WEIGHTS['appeal'])
    avg += float(self.new_product * WEIGHTS['new_product'])
    avg += float(self.new_store   * WEIGHTS['new_store'])
    return int(100 * avg / sum(WEIGHTS.values()))

  @property
  def weights_sum(self):
    from apps.public.controller.product_ranking import WEIGHTS
    sum = 0
    for key in WEIGHTS:
      sum += WEIGHTS[key]
    return sum

# MODEL FUNCTIONS