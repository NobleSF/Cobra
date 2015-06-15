from django.db import models
from apps.admin.utils.exception_handling import ExceptionHandler
from apps.seller.models.product import Product


class Rating(models.Model):

  [PHOTOGRAPHY, PRICE, APPEAL] = range(1, 4)
  SUBJECT_OPTIONS = ( # use name of icon in icon-font
    (PHOTOGRAPHY, 'photography'),
    (PRICE,       'price'),
    (APPEAL,      'appeal'),
  )
  subject             = models.SmallIntegerField(choices=SUBJECT_OPTIONS)
  product             = models.ForeignKey(Product)
  value               = models.SmallIntegerField()

  session_key         = models.CharField(max_length=32) #todo: tie to account of rater
  created_at          = models.DateTimeField(auto_now_add=True)

  # MODEL PROPERTIES
  # MODEL FUNCTIONS
  def __unicode__(self):
    return unicode(self.value)

#SIGNALS AND SIGNAL REGISTRATION
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete
from apps.public.models.ranking import Ranking

@receiver(post_save, sender=Rating)
def updateRatingRankings(sender, instance, created, **kwargs):
  from apps.public.views.product_ranking import newProductResult, newStoreResult, photographyResult, priceResult, appealResult
  try:
    ranking, is_new = Ranking.objects.get_or_create(product=instance.product)
    if is_new:
      ranking.new_product = newProductResult(instance.product)
      ranking.new_store   = newStoreResult(instance.product)

    if instance.subject == Rating.PHOTOGRAPHY:
      ranking.photography = photographyResult(instance.product)
    elif instance.subject == Rating.PRICE:
      ranking.price = priceResult(instance.product)
    elif instance.subject == Rating.APPEAL:
      ranking.appeal = appealResult(instance.product)
    ranking.save()
  except Exception as e:
    ExceptionHandler(e, "error on product_rankings.updateRatingRankings", no_email=True)
