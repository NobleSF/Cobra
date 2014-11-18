# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0007_checkout_currency_string'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkout',
            name='currency',
        ),
    ]
