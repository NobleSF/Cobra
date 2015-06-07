# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0008_move_country_model'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Color',
            new_name='OldColor',
        ),
    ]
