# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def saveRatingSubjects(apps, schema_editor):

  Rating = apps.get_model('public', 'Rating')
  RatingSubject = apps.get_model('admin', 'RatingSubject')
  [PHOTOGRAPHY, PRICE, APPEAL] = range(1, 4)

  for rating in Rating.objects.all():
    if rating.subject.name == "Photography":
      rating.new_subject = PHOTOGRAPHY
    elif rating.subject.name == "Price":
      rating.new_subject = PRICE
    elif rating.subject.name == "Appeal":
      rating.new_subject = APPEAL
    rating.save()

class Migration(migrations.Migration):

    dependencies = [
        ('public', '0031_rating_new_subject'),
    ]

    operations = [
        migrations.RunPython(saveRatingSubjects)
    ]
