from django.conf.urls import patterns, include, url
from controller import account, inventory, management

urlpatterns = patterns('',

  url(r'^$', management.home, name='management home'), #seller dashboard, live products
  url(r'^orders$', management.orders, name='management orders'), #orders
  url(r'^catalog$', management.catalog, name='management catalog'), #catalog
  url(r'^test$', management.test, name='management test'), #catalog

  url(r'^edit$', account.edit, name='edit'), #edit seller info
  url(r'^ajax/seller_save$', account.saveSeller, name='save seller'),
  url(r'^ajax/asset_save$', account.saveAsset, name='save asset'),
  url(r'^ajax/product_save$', inventory.saveProduct, name='save product'),

  url(r'^ajax/photo_form_data$', management.photoFormData, name='photo form data'),

  url(r'^inventory/create$', inventory.create, name='inventory create'),
  url(r'^inventory/(?P<product_id>\d+)$', inventory.detail, name='inventory detail'),
  url(r'^inventory/(?P<product_id>\d+)/edit$', inventory.edit, name='inventory edit'),
  url(r'^inventory/(?P<product_id>\d+)/delete$', inventory.delete, name='inventory delete'),
)
