import requests
from requests.auth import HTTPBasicAuth
from settings.settings import TELERIVET, DEBUG
import simplejson as json
import re #using to remove non-digits from phone numbers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apps.communication.models import SMS

def sendSMS(msg, to_number, priority='1'): #using Telerivet
  try:
    post_url =  'https://api.telerivet.com/v1/projects/'
    post_url += TELERIVET['project_id'] + '/messages/outgoing'
    authentication = HTTPBasicAuth(TELERIVET['api_key'], TELERIVET['api_key'])
    parameters = {
      'phone_id':       TELERIVET['phone_id'],
      'to_number':      to_number,
      'content':        msg,
      'message_type':   'sms',
      'priority':       priority,
      'status_url':     TELERIVET['status_url'],
      'status_secret':  TELERIVET['status_secret']
    }
    response = requests.post(post_url, auth=authentication, data=parameters)
    status_code = response.status_code
    response_content = json.loads(response.content) #dict of response content

  except Exception as e:
    return "error: " + str(e)

  else:
    if status_code == '200':
      return saveSMS(response_content) #responds True or exception str
    else:
      return "bad request or possible Telerivet error"

def saveSMS(sms_content): #takes Telerivet response content detail at
  #https://telerivet.com/p/PJ8973e6e346c349cbcdd094fcffa9fcb5/api/rest/sending
  try:
    sms = SMS(
      from_number   = re.sub("\D", "", sms_content['from_number']),
      to_number     = re.sub("\D", "", sms_content['to_number']),
      message       = sms_content['content'],
      telerivet_id  = sms_content['id'],
      status        = sms_content['status']
    )
    sms.save()
  except Exception as e:
    return "error: " + str(e)
  else:
    return True

@csrf_exempt
def incoming(request): #receives SMS messages via Telerivet, detail at
  #https://telerivet.com/p/PJ8973e6e346c349cbcdd094fcffa9fcb5/api/webhook/receiving
  from apps.public.controller.order_class import processOrderEvent
  from apps.communication.controller.events import updateOrder

  if TELERIVET['webhook_secret'] == request.POST.get('secret'):
    try:
      #save the SMS in db
      sms = SMS(
        telerivet_id  = request.POST['id'],
        from_number   = re.sub("\D", "", request.POST['from_number']),
        to_number     = re.sub("\D", "", request.POST['to_number']),
        message       = request.POST['content'],
      )
      sms.save()

      #look at what we received
      msg_data = understandMessage(request.POST['content'])
      #msg_data is tuple like (product_id, action, data) or
      #just False if not understandable

      if msg_data: #if it was understandable, send it to update the order
        reply_msg = updateOrder(msg_data, gimme_reply_sms=True)
        #gives us reply string, error string, or False

        if isinstance(reply_msg, basestring) and not reply_msg.startswith("error"):
          sms.auto_reply = reply_msg
          sms.save()
          #send reply back with response
          response = {'messages':[{'content':reply_msg}]}
          return HttpResponse(json.dumps(response), mimetype='application/json')

      else: #message not understandable
        #maybe they wanna chat or need help? send someone an email?
        return HttpResponse(status=200)#all good

    except Exception as e:
      if DEBUG:
        response = {'messages':[{'content':str(e)}]}
        return HttpResponse(json.dumps(response), mimetype='application/json')
      else:
        HttpResponse(status=500)#server error, our fault, Telerivet will try again

  else:
    return HttpResponse(status=403)#forbidden, didn't come from Telerivet

@csrf_exempt
def status_confirmation(request):
  #confirming that a sent SMS successfully reached it's recipient, detail at
  #https://telerivet.com/p/PJ8973e6e346c349cbcdd094fcffa9fcb5/api/webhook/status

  #don't care to check if it is a POST or has malformed data
  #because if it did it wouldn't have come from Telerivet

  if request.POST['secret'] == TELERIVET['status_secret']:
    sms = SMS.objects.get(telerivet_id=request.POST['id'])
    sms.status = request.POST['status']
    sms.save()
    return HttpResponse(status=200)
  else:
    return HttpResponse(status=403)

def understandMessage(message):
  #take a message and comprehend the desired action on a product id (or return False)

  return ('1234', 'shipped', {'tracking_number':"123456789"})
  #return False
