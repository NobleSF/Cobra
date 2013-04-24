from django.conf.urls import patterns, include, url
from controller import account, inventory

urlpatterns = patterns('',

  url(r'^$', account.home, name='home'), #seller dashboard
  url(r'^edit$', account.edit, name='edit'), #edit seller info

  url(r'^ajax/asset_save$', account.saveAsset, name='save asset'),
  url(r'^ajax/product_save$', inventory.saveProduct, name='save product'),

  url(r'^inventory$', inventory.home, name='inventory home'), #all products
  url(r'^inventory/create$', inventory.create, name='inventory create'),
  url(r'^inventory/(?P<product_id>\d+)$', inventory.detail, name='inventory detail'),
  url(r'^inventory/(?P<product_id>\d+)/edit$', inventory.edit, name='inventory edit'),
  url(r'^inventory/(?P<product_id>\d+)/delete$', inventory.delete, name='inventory delete'),
)
