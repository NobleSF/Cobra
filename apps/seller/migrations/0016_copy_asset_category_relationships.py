# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def copyColors(apps, schema_editor):
  Asset = apps.get_model('seller', 'Asset')
  OldCategory = apps.get_model('admin', 'OldCategory')
  NewCategory = apps.get_model('common', 'Category')

  for oldcat in OldCategory.objects.all():
    newcat, created = NewCategory.objects.get_or_create(
      name = oldcat.name,
      plural_name = oldcat.plural_name,
      keywords = oldcat.keywords,
      parent_category_id = oldcat.parent_category,
      ordering_name = oldcat.ordering_name
    )

  for asset in Asset.objects.all():
    for oldcat in asset.oldcategories.all():
      try:
        newcat = NewCategory.objects.get(name=oldcat.name)
        asset.newcategories.add(newcat)
      except Exception as e:
        print str(e)


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0015_asset_newcategories'),
        ('common', '0005_category_self_relationship'),
    ]

    operations = [
        migrations.RunPython(copyColors)
    ]
