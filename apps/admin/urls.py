from django.conf.urls import patterns, include, url
from controller import account, dashboard

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

#account pages
urlpatterns = patterns('',
  #Todo: I'd like to add the word "secure" into all account and checkout pages
    # just to give the user more peace of mind.

  url(r'^account/create$', account.create, name='account create'),
  url(r'^account/edit$', account.edit, name='account edit'),
  url(r'^account/login$', account.login, name='login'),
  url(r'^account/logout$', account.logout, name='logout'),
  url(r'^account/(?P<username>\w+)$', account.home, name='account'),
)

#dashboard pages
urlpatterns += patterns('',
  url(r'^admin/dashboard$', dashboard.home, name='home'),
  url(r'^admin/dashboard/country$', dashboard.country, name='country'),
  url(r'^admin/dashboard/currency$', dashboard.currency, name='currency'),
  url(r'^admin/dashboard/color$', dashboard.color, name='color'),
  url(r'^admin/admin/dashboard/category$', dashboard.category, name='category'),
  url(r'^dashboard/rating_subject$', dashboard.rating_subject, name='rating_subject'),
  url(r'^dashboard/shipping_option$', dashboard.shipping_option, name='shipping_option'),
  url(r'^dashboard/image_object$', dashboard.image_object, name='image_object'),
)
