from django.http import HttpResponse
import json
from apps.communication.controllers.email_class import Email
from apps.communication.controllers.sms import sendSMS
from settings.settings import DEBUG
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def subscribe(request): #ajax requests only
  from django.db import IntegrityError, transaction
  from apps.communication.models.subscription import Subscription
  try:
    subscription = Subscription(email=request.GET.get('email'))
    if request.GET.get('name'):
      subscription.name = request.GET.get('name')
    subscription.save()
    response = {'success': "%s is subscribed" % subscription.email}

    Email("subscription/new").sendTo(subscription.email)

  except IntegrityError: #already subscribed
    if request.GET.get('name'):
      try: transaction.rollback()
      except: pass
      try:
        subscription = Subscription.objects.get(email=request.GET.get('email'))
        subscription.name = request.GET.get('name')
        subscription.save()
      except: pass
    response = {'success': "%s already subscribed" % subscription.email}

  except Exception as e:
    response = {'exception': str(e)}

  return HttpResponse(json.dumps(response), content_type='application/json')

def communicateSubscribed():
  return True

def unsubscribe(request):
  pass

def communicateUnsubscribed():
  pass

from apps.admin.utils.decorator import access_required
@access_required('admin')
def test_email():
  from django.core.mail import send_mail
  send_mail('Subject here', 'Here is the message.', 'hello@theanou.com', ['dev+test@theanou.com'], fail_silently=False)
