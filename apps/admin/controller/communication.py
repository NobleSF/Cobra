from django.http import HttpResponse
from django.shortcuts import render
from apps.admin.controller.decorator import access_required
from django.contrib import messages
from django.utils import simplejson
from datetime import datetime
from apps.communication.models import SMS

@access_required('admin')
def sendSMS(request):
  from apps.admin.controller.forms import SMSForm
  from apps.communication.controller.sms import sendSMS

  if request.method == 'POST':
    to_number = request.POST.get('to_number')
    message   = request.POST.get('message')
    sendSMS(message, to_number)
    messages.success(request, "SMS sent!")

  return render(request, 'communication/send_sms.html', {'form': SMSForm()})

def allSMS(request):
  from settings.settings import TELERIVET
  context = {
              'sms_messages': SMS.objects.all().order_by('created_at').reverse(),
              'anou_phone':   TELERIVET['phone_number']
            }
  return render(request, 'communication/all_sms.html', context)


def allEmail():
  pass
