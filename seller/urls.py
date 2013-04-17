from django.conf.urls import patterns, include, url
from controller import account, inventory

urlpatterns = patterns('',

  url(r'^$', account.home, name='home'), #seller dashboard
  url(r'^edit$', account.edit, name='edit'), #edit seller info

  url(r'^ajax/asset_save$', account.saveAsset, name='save asset'),
  url(r'^ajax/image_save$', account.saveImage, name='save image'),
# url(r'^ajax/photo_save$', account.savePhoto, name='save photo'),

  url(r'^inventory$', inventory.home, name='inventory home'), #all products
  url(r'^inventory/create$', inventory.create, name='inventory create'),
  url(r'^inventory/(?P<id>\d+)$', inventory.detail, name='inventory detail'),
  url(r'^inventory/(?P<id>\d+)/edit$', inventory.edit, name='inventory edit'),
  url(r'^inventory/(?P<id>\d+)/delete$', inventory.delete, name='inventory delete'),
)
