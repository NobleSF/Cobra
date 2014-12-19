# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0018_auto_20141219_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commission',
            name='customer',
            field=models.ForeignKey(related_name='commissions', to='public.Customer', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='commission',
            name='product',
            field=models.OneToOneField(related_name='commission', null=True, to='seller.Product'),
            preserve_default=True,
        ),
    ]
