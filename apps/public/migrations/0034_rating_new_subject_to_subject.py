# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0033_remove_rating_subject'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='new_subject',
            new_name='subject',
        ),
    ]
