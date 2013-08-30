from django.http import HttpResponse
from django.shortcuts import render
from apps.admin.controller.decorator import access_required
from django.contrib import messages
from django.utils import simplejson
from datetime import datetime
from apps.communication.models import SMS, Email
from apps.seller.models import Seller

@access_required('admin')
def allSMS(request):
  from settings.settings import TELERIVET
  from apps.admin.controller.forms import SMSForm
  from apps.communication.controller.sms import sendSMS

  if request.method == 'POST':
    to_number = request.POST.get('to_number')
    message   = request.POST.get('message')
    order_id  = request.POST.get('order')

    sms = sendSMS(message, to_number)
    if isinstance(sms, SMS):
      try:
        if order_id:
          sms.order_id = order_id
          sms.save()
      except:
        messages.warning(request, "SMS sent, but order# invalid.")
      else:
        messages.success(request, "SMS sent!")
    else:
      messages.error(request, "SMS failed!")
      context['except'] = str(sms)

  sms_messages = SMS.objects.all().order_by('created_at').reverse()[:100]

  for sms in sms_messages:
    if sms.from_number == TELERIVET['phone_number']:
      sms.phone_number = sms.to_number
      sms.incoming = False
    else:
      sms.phone_number = sms.from_number
      sms.incoming = True

    try:
      sms.seller = Seller.objects.get(account__phone=sms.phone_number)
    except: pass

  context = {
              'form':         SMSForm(),
              'sms_messages': sms_messages,
              'anou_phone':   TELERIVET['phone_number']
            }
  return render(request, 'communication/all_sms.html', context)

@access_required('admin')
def allEmail(request):

  emails = Email.objects.all().order_by('created_at').reverse()[:100]

  for email in emails:
    try:
      email.seller = Seller.objects.get(account__email=email.to_address)
    except: pass

  context = {'emails':emails}
  return render(request, 'communication/all_email.html', context)
