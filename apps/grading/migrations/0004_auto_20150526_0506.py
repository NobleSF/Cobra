# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grading', '0003_auto_20150525_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actiontype',
            name='type',
            field=models.SmallIntegerField(unique=True, choices=[(1, b'product-add'), (2, b'product-edit'), (3, b'product-suspended'), (4, b'sms-order'), (5, b'sms-shipping'), (6, b'rating-photography'), (7, b'rating-appeal'), (8, b'rating-appeal'), (9, b'customer-rating-product'), (10, b'customer-rating-packaging'), (11, b'problem-call'), (12, b'instagram')]),
        ),
    ]
