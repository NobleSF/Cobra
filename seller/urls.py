from django.conf.urls import patterns, include, url
from controller import account, product

urlpatterns = patterns('',

  url(r'^$', account.home, name='home'), #seller dashboard
  url(r'^edit$', account.edit, name='edit'), #edit seller info

  url(r'^ajax/asset_save$', account.saveAsset, name='save asset'),
  url(r'^ajax/image_save$', account.saveImage, name='save image'),
# url(r'^ajax/photo_save$', account.savePhoto, name='save photo'),

  url(r'^product$', product.home, name='product home'), #all products
  url(r'^product/create$', product.create, name='product create'),
  url(r'^product/(?P<id>\d+)$', product.detail, name='product detail'),
  url(r'^product/(?P<id>\d+)/edit$', product.edit, name='product edit'),
  url(r'^product/(?P<id>\d+)/delete$', product.delete, name='product delete'),
)
