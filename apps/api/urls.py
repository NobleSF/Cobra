from django.conf.urls import patterns, include, url
from controller import home, checkout, product, store, custom_order

urlpatterns = patterns('',

  url(r'^scrollfood$', browsing.more_products, name='yum food'),

  url(r'^rating$', rating.rating, name='i heart you'),

  url(r'^listing$', listing.listing, name='listing'),
  url(r'^product$', product.product, name='product'),
  #url(r'^product/(?P<product_id>\d+)$', product.product, name='product'),

  #url(r'^store/(?P<store_id>\d+)$', store.store, name='store'),

)
