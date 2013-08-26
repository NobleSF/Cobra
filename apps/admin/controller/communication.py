from django.http import HttpResponse
from django.shortcuts import render
from apps.admin.controller.decorator import access_required
from django.contrib import messages
from django.utils import simplejson
from datetime import datetime
from apps.communication.models import SMS, Email
from apps.seller.models import Seller

@access_required('admin')
def sendSMS(request):
  from apps.admin.controller.forms import SMSForm
  from apps.communication.controller.sms import sendSMS

  if request.method == 'POST':
    to_number = request.POST.get('to_number')
    message   = request.POST.get('message')
    sms = sendSMS(message, to_number)
    if isinstance(sms, SMS):
      messages.success(request, "SMS sent!")
    else:
      messages.error(request, "SMS failed!")

  return render(request, 'communication/send_sms.html', {'form': SMSForm()})

def allSMS(request):
  from settings.settings import TELERIVET

  sms_messages = SMS.objects.all().order_by('created_at').reverse()[:100]

  for sms in sms_messages:
    if sms.from_number == TELERIVET['phone_number']:
      sms.phone_number = sms.to_number
    else:
      sms.phone_number = sms.from_number

    try:
      sms.seller = Seller.objects.get(account__phone=sms.phone_number)
    except: pass

  context = {
              'sms_messages': sms_messages,
              'anou_phone':   TELERIVET['phone_number']
            }
  return render(request, 'communication/all_sms.html', context)


def allEmail(request):

  emails = Email.objects.all().order_by('created_at').reverse()[:100]

  for email in emails:
    try:
      email.seller = Seller.objects.get(account__email=email.to_address)
    except: pass

  context = {'emails':emails}
  return render(request, 'communication/all_email.html', context)
