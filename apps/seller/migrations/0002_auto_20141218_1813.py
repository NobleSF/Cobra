# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customorder',
            name='base_product',
        ),
        migrations.RemoveField(
            model_name='customorder',
            name='custom_product',
        ),
        migrations.DeleteModel(
            name='CustomOrder',
        ),
    ]
