from math import log, pow, e, ceil
from django.db.models import Avg
from datetime import datetime

WEIGHTS = {'date_posted': 12,
           'photography': 10,
           'price':       5,
           'appeal':      8,
           'new_store':   6
          }
DAYS_TO_PROMOTE_NEW_PRODUCT = 2
DAYS_TO_PROMOTE_NEW_STORE = 14

def getRankPoints(product):
  sum = 0.0
  sum += datePostedResult(product)
  sum += photographyResult(product)
  sum += priceResult(product)
  sum += appealResult(product)
  sum += storeNewnessResult(product)

  points = 100 * sum / sumWeights()
  return int(points)

def datePostedResult(product):
  W = float(WEIGHTS['date_posted'])
  V = float(datePostedValue(product))
  C = 1.00
  return createResult(W,V,C)

def datePostedValue(product):
  date_posted = product.approved_at.replace(tzinfo=None)
  time_difference = datetime.today() - date_posted
  this_number = time_difference.days - DAYS_TO_PROMOTE_NEW_PRODUCT
  this_number = 1 if this_number < 0 else this_number + 4
  value = 1.8 * invLog(this_number) if this_number > 1 else 1
  return value if value < 1 else 1

def photographyResult(product):
  ratingQuery = (product.rating_set.filter(subject__name='Photography')
                                   .aggregate(average=Avg('value')))
  numRatings = product.rating_set.filter(subject__name='Photography').count()

  W = float(WEIGHTS['photography'])
  V = float(ratingQuery['average'] / 5) if ratingQuery['average'] else 3
  C = float(ratingConfidence(numRatings)) if numRatings else 0
  return createResult(W,V,C)

def priceResult(product):
  ratingQuery = (product.rating_set.filter(subject__name='Price')
                                   .aggregate(average=Avg('value')))
  numRatings = product.rating_set.filter(subject__name='Price').count()

  W = float(WEIGHTS['price'])
  V = float(ratingQuery['average'] / 5) if ratingQuery['average'] else 3
  C = float(ratingConfidence(numRatings)) if numRatings else 0
  return createResult(W,V,C)

def appealResult(product):
  ratingQuery = (product.rating_set.filter(subject__name='Appeal')
                                   .aggregate(average=Avg('value')))
  numRatings = product.rating_set.filter(subject__name='Appeal').count()

  W = float(WEIGHTS['appeal'])
  V = float(ratingQuery['average'] / 5) if ratingQuery['average'] else 3
  C = float(ratingConfidence(numRatings)) if numRatings else 0
  return createResult(W,V,C)

def storeNewnessResult(product):
  W = float(WEIGHTS['new_store'])
  V = float(storeNewnessValue(product))
  C = 1.00
  return createResult(W,V,C)

def storeNewnessValue(product):
  date_live = product.seller.created_at.replace(tzinfo=None)
  time_difference = datetime.today() - date_live
  this_number = time_difference.days - DAYS_TO_PROMOTE_NEW_STORE
  this_number = 1 if this_number < 0 else this_number + 4
  value = 1.8 * invLog(this_number) if this_number > 1 else 1
  return value if value < 1 else 1

def ratingConfidence(numRatings):
  numRatings = float(numRatings) if numRatings > 3 else 3.0
  return 1 - (invLog((numRatings-2)*2) / 2)

def createResult(W,V,C): #let's make magic, baby!
  return W * (pow((V + 0.55), pow(C,2)))

def sumWeights():
  sum = 0
  for key in WEIGHTS:
    sum += WEIGHTS[key]
  return sum

def invLog(value):
  return 1/log(value*e)
