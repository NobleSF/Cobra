from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from apps.api.controllers import listing

urlpatterns = patterns('',

  #url(r'^scrollfood$', browsing.more_products, name='yum food'),

  #url(r'^rating$', rating.rating, name='i heart you'),

  #url(r'^listing$', listing.listing, name='listing'),
  #url(r'^product$', product.product, name='product'),
  #url(r'^product/(?P<product_id>\d+)$', product.product, name='product'),

  #url(r'^store/(?P<store_id>\d+)$', store.store, name='store'),

)


urlpatterns += patterns('',
  url(r'^listings/$', listing.ListingList.as_view(), name='listings'),
  url(r'^listings/(?P<product_id>[0-9]+)/$', listing.ListingDetail.as_view(), name='listing'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
