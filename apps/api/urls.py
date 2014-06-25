from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from apps.api.controllers import listing, store

urlpatterns = patterns('',
  url(r'^listings/$', listing.ListingList.as_view(), name='listings'),
  url(r'^listings/(?P<pk>[0-9]+)/$', listing.ListingDetail.as_view(), name='listing'),

  url(r'^stores/$', store.StoreList.as_view(), name='stores'),
  url(r'^stores/(?P<pk>[0-9]+)/$', store.StoreDetail.as_view(), name='store'),

  #Ratings
)

urlpatterns = format_suffix_patterns(urlpatterns)
