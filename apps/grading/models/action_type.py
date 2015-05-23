from django.db import models


class ActionType(models.Model):
  # ACTION TYPES, ONLY ONE OF EACH TYPE ALLOWED
  ( ADD_PRODUCT, EDIT_PRODUCT,
    SUSPENDED_PRODUCT,
    ORDER_SMS, SHIPPING_SMS,
    PHOTOGRAPHY_RATING, PRICE_RATING, APPEAL_RATING,
    CUSTOMER_PRODUCT_RATING, CUSTOMER_PACKAGING_RATING,
    PROBLEM_CALL,
    INSTAGRAM_PHOTO,
    #only add new types to end of list
  ) = range(12)

  TYPE_OPTIONS = ( # use name of icon in icon-font
    (ADD_PRODUCT,         'product-add'),
    (EDIT_PRODUCT,        'product-edit'),
    (SUSPENDED_PRODUCT,   'product-suspended'),
    (ORDER_SMS,           'sms-order'),
    (SHIPPING_SMS,        'sms-shipping'),
    (PHOTOGRAPHY_RATING,  'rating-photography'),
    (PRICE_RATING,        'rating-appeal'),
    (APPEAL_RATING,       'rating-appeal'),
    (CUSTOMER_PRODUCT_RATING, 'customer-rating-product'),
    (CUSTOMER_PACKAGING_RATING, 'customer-rating-packaging'),
    (PROBLEM_CALL,        'problem-call'),
    (INSTAGRAM_PHOTO,     'instagram'),
  )
  type            = models.SmallIntegerField(choices=TYPE_OPTIONS, unique=True)

  max_points      = models.BigIntegerField()
  #max_points = best point value of the action, 100% compliance with action type

  has_spread      = models.BooleanField(default=False)
  min_points      = models.BigIntegerField(null=True, blank=True)
  #min_points = worst point value of the action, 0% compliance with action type

  count_limit     = models.SmallIntegerField(default=0)
  # count_limit is number of actions per month
  # of it's type that can count towards total score,
  # 0 is no limit

  is_penalty      = models.BooleanField(default=False)
  #is_penalty = always a penalty, point value is always a negative number

  @property
  def name(self):
    return self.get_type_display()

  @property
  def icon_name(self):
    return self.get_type_display()
