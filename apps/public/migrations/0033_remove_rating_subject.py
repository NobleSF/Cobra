# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0032_migrate_rating_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='subject',
        ),
    ]
