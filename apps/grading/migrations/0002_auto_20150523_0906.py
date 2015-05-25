# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations

( ADD_PRODUCT, EDIT_PRODUCT,
  SUSPENDED_PRODUCT,
  ORDER_SMS, SHIPPING_SMS,
  PHOTOGRAPHY_RATING, PRICE_RATING, APPEAL_RATING,
  CUSTOMER_PRODUCT_RATING, CUSTOMER_PACKAGING_RATING,
  PROBLEM_CALL,
  INSTAGRAM_PHOTO,
  #only add new types to end of list
) = range(1, 13)

def create_action_types(apps, schema_editor):
  ActionType = apps.get_model("grading", "ActionType")

  # ADD_PRODUCT
  action_type = ActionType(type=ADD_PRODUCT)
  action_type.has_spread = False
  action_type.max_points = 5
  action_type.count_limit = 6
  action_type.is_penalty = False
  action_type.save()

  # EDIT_PRODUCT
  action_type = ActionType(type=EDIT_PRODUCT)
  action_type.has_spread = False
  action_type.max_points = 5
  action_type.count_limit = 6
  action_type.is_penalty = False
  action_type.save()

  # SUSPENDED_PRODUCT
  action_type = ActionType(type=SUSPENDED_PRODUCT)
  action_type.has_spread = False
  action_type.max_points = -1
  action_type.count_limit = 0
  action_type.is_penalty = True
  action_type.save()

  # PHOTOGRAPHY_RATING
  action_type = ActionType(type=PHOTOGRAPHY_RATING)
  action_type.has_spread = True
  action_type.max_points = 14
  action_type.min_points = -14
  action_type.count_limit = ActionType.objects.get(type=ADD_PRODUCT).count_limit
  action_type.is_penalty = False
  action_type.save()

  # PRICE_RATING
  action_type = ActionType(type=PRICE_RATING)
  action_type.has_spread = True
  action_type.max_points = 14
  action_type.min_points = -14
  action_type.count_limit = ActionType.objects.get(type=ADD_PRODUCT).count_limit
  action_type.is_penalty = False
  action_type.save()

  # APPEAL_RATING
  action_type = ActionType(type=APPEAL_RATING)
  action_type.has_spread = True
  action_type.max_points = 14
  action_type.min_points = -14
  action_type.count_limit = ActionType.objects.get(type=ADD_PRODUCT).count_limit
  action_type.is_penalty = False
  action_type.save()

  # ORDER_SMS
  action_type = ActionType(type=ORDER_SMS)
  action_type.has_spread = True
  action_type.max_points = 30
  action_type.min_points = -30
  action_type.count_limit = 0
  action_type.is_penalty = False
  action_type.save()

  # SHIPPING_SMS
  action_type = ActionType(type=SHIPPING_SMS)
  action_type.has_spread = True
  action_type.max_points = 50
  action_type.min_points = -30
  action_type.count_limit = 0
  action_type.is_penalty = False
  action_type.save()

  # CUSTOMER_PRODUCT_RATING
  action_type = ActionType(type=CUSTOMER_PRODUCT_RATING)
  action_type.has_spread = True
  action_type.max_points = 30
  action_type.min_points = -20
  action_type.count_limit = 0
  action_type.is_penalty = False
  action_type.save()

  # CUSTOMER_PACKAGING_RATING
  action_type = ActionType(type=CUSTOMER_PACKAGING_RATING)
  action_type.has_spread = True
  action_type.max_points = 40
  action_type.min_points = -40
  action_type.count_limit = 0
  action_type.is_penalty = False
  action_type.save()

  # PROBLEM_CALL
  action_type = ActionType(type=PROBLEM_CALL)
  action_type.has_spread = False
  action_type.max_points = -5
  action_type.count_limit = 10
  action_type.is_penalty = True
  action_type.save()

  # INSTAGRAM_PHOTO
  action_type = ActionType(type=INSTAGRAM_PHOTO)
  action_type.has_spread = False
  action_type.max_points = 5
  action_type.count_limit = 0
  action_type.is_penalty = False
  action_type.save()


class Migration(migrations.Migration):

    dependencies = [
        ('grading', '0001_initial'),
    ]

    operations = [
         migrations.RunPython(create_action_types),
    ]
