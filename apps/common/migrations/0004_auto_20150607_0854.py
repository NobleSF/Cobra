# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_newcolor'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NewColor',
            new_name='Color',
        ),
    ]
