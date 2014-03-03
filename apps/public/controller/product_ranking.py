from math import log, pow, e, ceil
from django.db.models import Avg
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.seller.models.product import Product
from apps.public.models import Rating, Ranking
from apps.admin.utils.exception_handling import ExceptionHandler

WEIGHTS = {'photography': 14,
           'price':       5,
           'appeal':      8,
           'new_product': 6,
           'new_store':   4
          }
DAYS_TO_PROMOTE_NEW_PRODUCT = 2
DAYS_TO_PROMOTE_NEW_STORE   = 14

def updateRankings(product, except_ratings=False):
  try:
    ranking, is_new = Ranking.objects.get_or_create(product=product)
    ranking.new_product = newProductResult(product)
    ranking.new_store = newStoreResult(product)
    if not except_ratings:
      ranking.photography = photographyResult(product)
      ranking.price = priceResult(product)
      ranking.appeal = appealResult(product)
    ranking.save()
  except Exception as e:
    ExceptionHandler(e, "error on product_rankings.updateRankings", sentry_only=True)

def photographyResult(product):
  try:
    ratings = (product.rating_set.filter(subject__name='Photography')
                                     .aggregate(average=Avg('value')))
    num_ratings = product.rating_set.filter(subject__name='Photography').count()

    V = float(ratings['average']-1) / 4 if ratings['average'] >= 1 else 0.5
    C = float(ratingConfidence(num_ratings)) if num_ratings else 0
    return createResult(V,C)
  except:
    return 0.5

def priceResult(product):
  try:
    ratings = (product.rating_set.filter(subject__name='Price')
                                     .aggregate(average=Avg('value')))
    num_ratings = product.rating_set.filter(subject__name='Price').count()

    V = float(ratings['average']-1) / 4 if ratings['average'] >= 1 else 0.5
    C = float(ratingConfidence(num_ratings)) if num_ratings else 0
    return createResult(V,C)
  except:
    return 0.5

def appealResult(product):
  try:
    ratings = (product.rating_set.filter(subject__name='Appeal')
                                     .aggregate(average=Avg('value')))
    num_ratings = product.rating_set.filter(subject__name='Appeal').count()

    V = float(ratings['average']-1) / 4 if ratings['average'] >= 1 else 0.5
    C = float(ratingConfidence(num_ratings)) if num_ratings else 0
    return createResult(V,C)
  except:
    return 0.5

def newProductResult(product):
  try:
    V = float(newProductValue(product))
    C = 1.00
    return createResult(V,C)
  except:
    return 0.5

def newProductValue(product):
  time_difference = timezone.now() - product.approved_at
  this_number = time_difference.days - DAYS_TO_PROMOTE_NEW_PRODUCT
  this_number = 1 if this_number < 0 else this_number + 4
  value = 1.8 * invLog(this_number) if this_number > 1 else 1
  return value if value < 1 else 1

def newStoreResult(product):
  try:
    V = float(newStoreValue(product))
    C = 1.00
    return createResult(V,C)
  except:
    return 0.5

def newStoreValue(product):
  time_difference = timezone.now() - product.seller.created_at
  this_number = time_difference.days - DAYS_TO_PROMOTE_NEW_STORE
  this_number = 1 if this_number < 0 else this_number + 4
  value = 1.8 * invLog(this_number) if this_number > 1 else 1
  return value if value < 1 else 1

def ratingConfidence(num_ratings):
  num_ratings = float(num_ratings) if num_ratings > 3 else 3.0
  return 1 - (invLog((num_ratings-2)*2) / 2)

def createResult(V, C):
  # Value usually within range[0,1]
  # Confindence always within range [0,1]
  # (V+.55)^(C^2)
  return pow((V + 0.55), pow(C,2))

def invLog(value):
  return 1/log(value*e)
