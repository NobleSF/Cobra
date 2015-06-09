# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0010_delete_oldcolor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parent_category',
            field=models.IntegerField(null=True),
        ),
    ]
