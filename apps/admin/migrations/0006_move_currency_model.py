# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0005_auto_20150607_0702'),
    ]

    database_operations = [
        migrations.AlterModelTable('Currency', 'common_currency')
    ]

    state_operations = [
        migrations.DeleteModel('Currency')
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations,
            state_operations=state_operations)
    ]
