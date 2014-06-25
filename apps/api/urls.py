from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from apps.api.controllers import listing, store, category

urlpatterns = patterns('',
  url(r'^listings/$', listing.ListingList.as_view(), name='listings'),
  url(r'^listings/(?P<pk>[0-9]+)/$', listing.ListingDetail.as_view(), name='listing'),

  url(r'^stores/$', store.StoreList.as_view(), name='stores'),
  url(r'^stores/(?P<pk>[0-9]+)/$', store.StoreDetail.as_view(), name='store'),

  url(r'^categories/$', category.CategoryList.as_view(), name='categories'),
  url(r'^categories/(?P<pk>[0-9]+)/$', category.CategoryDetail.as_view(), name='category'),

  #Ratings
)

urlpatterns = format_suffix_patterns(urlpatterns)
