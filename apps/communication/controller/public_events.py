from django.http import HttpResponse
from django.utils import simplejson
from apps.communication.controller.email_class import Email
from apps.communication.controller.sms import sendSMS
from settings.settings import DEBUG

def subscribe(request): #ajax requests only
  from django.db import IntegrityError
  from apps.public.models import Subscription
  try:
    subscription = Subscription(email=request.GET.get('email'))
    if request.GET.get('name'):
      subscription.name = request.GET.get('name')
    subscription.save()
    response = {'success': "%s is subscribed" % subscription.email}

  except IntegrityError: #already subscribed
    if request.GET.get('name'):
      subscription = Subscription.objects.get(email=request.GET.get('email'))
      subscription.name = request.GET.get('name')
      subscription.save()
    response = {'success': "%s already subscribed" % subscription.email}

  except Exception as e:
    response = {'exception': str(e)}

  return HttpResponse(simplejson.dumps(response), mimetype='application/json')

def communicateSubscribed():
  return True

def unsubscribe(request):
  pass

def communicateUnsubscribed():
  pass

from apps.admin.controller.decorator import access_required
@access_required('admin')
def test_email():
  from django.core.mail import send_mail
  send_mail('Subject here', 'Here is the message.', 'hello@theanou.com', ['dev+test@theanou.com'], fail_silently=False)
