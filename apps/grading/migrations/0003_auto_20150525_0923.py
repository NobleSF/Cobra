# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0005_auto_20150520_0803'),
        ('grading', '0002_auto_20150523_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='product',
            field=models.ForeignKey(related_name='actions', to='seller.Product', null=True),
        ),
        migrations.AlterField(
            model_name='actiontype',
            name='type',
            field=models.SmallIntegerField(unique=True, choices=[(0, b'product-add'), (1, b'product-edit'), (2, b'product-suspended'), (3, b'sms-order'), (4, b'sms-shipping'), (5, b'rating-photography'), (6, b'rating-appeal'), (7, b'rating-appeal'), (8, b'customer-rating-product'), (9, b'customer-rating-packaging'), (10, b'problem-call'), (11, b'instagram')]),
        ),
    ]
