# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0008_remove_checkout_currency'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkout',
            old_name='currency_string',
            new_name='currency',
        ),
    ]
