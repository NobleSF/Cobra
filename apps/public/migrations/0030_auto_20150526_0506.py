# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0029_auto_20150522_0833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commission',
            name='base_product',
        ),
        migrations.RemoveField(
            model_name='commission',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='commission',
            name='product',
        ),
        migrations.RemoveField(
            model_name='commission',
            name='requirement_images',
        ),
        migrations.DeleteModel(
            name='Commission',
        ),
    ]
