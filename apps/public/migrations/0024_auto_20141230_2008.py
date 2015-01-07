# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0023_commission_progression'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commission',
            old_name='progression',
            new_name='progress',
        ),
        migrations.RenameField(
            model_name='commission',
            old_name='in_progress_at',
            new_name='progress_updated_at',
        ),
    ]
