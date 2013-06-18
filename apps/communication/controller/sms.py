import requests
from requests.auth import HTTPBasicAuth
from settings.settings import TELERIVET
import simplejson as json

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
    return str(e)

  else:
    if status_code == '200':
      return saveSMS(response_content)
    else:
      return False

def saveSMS(sms_content): #takes Telerivet response content detail at
  #https://telerivet.com/p/PJ8973e6e346c349cbcdd094fcffa9fcb5/api/rest/sending
  from apps.communication.models import SMS
  try:
    sms = SMS(
      from_number = sms_content['from_number'],
      to_number   = sms_content['to_number'],
      message     = sms_content['content'],
      status      = sms_content['status']
    )
    sms.save()
  except Exception as e:
    return str(e)
  else:
    return True

def incoming():
  #using telerivet:
  #https://telerivet.com/p/PJ8973e6e346c349cbcdd094fcffa9fcb5/api/webhook/receiving
  pass

def status_confirmation():
  #confirming that a sent SMS successfully reached it's recipient
  pass