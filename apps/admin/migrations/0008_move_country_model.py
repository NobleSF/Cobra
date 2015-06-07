# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0007_auto_20150607_0730'),
        ('seller', '0006_auto_20150607_0736'),
    ]

    database_operations = [
        migrations.AlterModelTable('Country', 'common_country')
    ]

    state_operations = [
        migrations.DeleteModel('Country')
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations,
            state_operations=state_operations)
    ]