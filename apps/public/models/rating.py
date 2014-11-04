from django.db import models
from apps.seller.models.product import Product
from apps.admin.models.rating_subject import RatingSubject

class Rating(models.Model):
  session_key         = models.CharField(max_length=32)
  #todo: tie to account
  product             = models.ForeignKey(Product)
  subject             = models.ForeignKey(RatingSubject)
  value               = models.SmallIntegerField()
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
  from apps.public.controller.product_ranking import newProductResult, newStoreResult, photographyResult, priceResult, appealResult
  try:
    ranking, is_new = Ranking.objects.get_or_create(product=instance.product)
    if is_new:
      ranking.new_product = newProductResult(instance.product)
      ranking.new_store   = newStoreResult(instance.product)

    if instance.subject.name == 'Photography':
      ranking.photography = photographyResult(instance.product)
    elif instance.subject.name == 'Price':
      ranking.price = priceResult(instance.product)
    elif instance.subject.name == 'Appeal':
      ranking.appeal = appealResult(instance.product)
    ranking.save()
  except Exception as e:
    ExceptionHandler(e, "error on product_rankings.updateRatingRankings", sentry_only=True)
