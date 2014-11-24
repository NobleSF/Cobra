# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0012_auto_20141124_1549'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkout',
            old_name='checkout_data',
            new_name='payment_data',
        ),
        migrations.RenameField(
            model_name='checkout',
            old_name='checkout_id',
            new_name='payment_id',
        ),
    ]
