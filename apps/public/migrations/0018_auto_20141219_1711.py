# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0017_auto_20141218_1813'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commission',
            old_name='estimated_price',
            new_name='estimated_display_price',
        ),
        migrations.AlterField(
            model_name='commission',
            name='customer',
            field=models.ForeignKey(related_name='commissions', to='public.Customer'),
            preserve_default=True,
        ),
    ]
