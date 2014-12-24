# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0020_auto_20141219_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commission',
            name='product',
            field=models.OneToOneField(related_name='commission', null=True, to='seller.Product'),
            preserve_default=True,
        ),
    ]
