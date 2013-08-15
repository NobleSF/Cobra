from django.http import HttpResponse
from django.shortcuts import render
from apps.admin.controller.decorator import access_required
from django.contrib import messages
from django.utils import simplejson
from datetime import datetime

@access_required('admin')
def sms(request):
  from apps.admin.controller.forms import SMSForm
  from apps.communication.controller.sms import sendSMS

  if request.method == 'POST':
    to_number = request.POST.get('to_number')
    message   = request.POST.get('message')
    sendSMS(message, to_number)
    messages.success(request, "SMS sent!")

  return render(request, 'communication/sms.html', {'form': SMSForm()})
