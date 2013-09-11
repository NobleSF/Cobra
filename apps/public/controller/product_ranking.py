from math import log, pow, e, ceil
from django.db.models import Avg
from datetime import datetime

WEIGHTS = {'date_posted': 15,
           'photography': 10,
           'price':       5,
           'appeal':      8,
           'new_store':   6
          }

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
  difference = datetime.today() - date_posted
  value = 1.8 * invLog(float(difference.days)) if difference.days > 1 else 1
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
  difference = datetime.today() - date_live
  value = 1.8 * invLog(float(difference.days-12)) if difference.days > 12 else 1
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
