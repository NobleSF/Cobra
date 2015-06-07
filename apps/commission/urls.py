from django.conf.urls import url
from apps.commission.views import commission

urlpatterns = [

  #COMMISSIONS
  url(r'^find_commission/$', commission.find_commission, name='find'),
  url(r'^commissions$', commission.commissions, name='commissions'),
  url(r'^commission/create$', commission.create, name='create commission'),
  url(r'^commission/(?P<commission_id>\d+)$', commission.commission, name='commission'),
  url(r'^commission/requirement_image_form_data$', commission.imageFormData, name='commission image'),
  url(r'^commission/progress_photo_form_data$', commission.imageFormData, name='commission photo'),

]
