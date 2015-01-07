# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0002_auto_20141218_1813'),
        ('public', '0021_auto_20141219_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='commission',
            name='requirement_images',
            field=models.ManyToManyField(to='seller.Image'),
            preserve_default=True,
        ),
    ]
