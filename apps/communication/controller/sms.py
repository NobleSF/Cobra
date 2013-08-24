import requests
from requests.auth import HTTPBasicAuth
from settings.settings import TELERIVET, DEBUG
import simplejson as json
import re #regular expressions
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apps.communication.models import SMS
from apps.seller.models import Product
from apps.admin.controller.decorator import postpone

@postpone
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
    response_content = json.loads(response.content) #dict of response content

  except Exception as e:
    return "error: " + str(e)

  else:
    if int(response.status_code) is 200:
      return saveSMS(response_content) #responds with SMS object or exception str
    else:
      return "bad request or possible Telerivet error"

def sendSMSForOrder(msg, to_number, order, priority='1'):
  try:
    sms = sendSMS(msg, to_number, priority)
    if isinstance(sms, SMS):
      sms.order = order
      sms.save()
    return sms
  except Exception as e:
    return "error: " + str(e)

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
    return sms

@csrf_exempt
def incoming(request):
  """ receives SMS messages via Telerivet, detail at
      https://telerivet.com/p/PJ8973e6e346c349cbcdd094fcffa9fcb5/api/webhook/receiving
  """
  from apps.communication.controller import order_events, seller_events

  if TELERIVET['webhook_secret'] == request.POST.get('secret'):
    """
        Step 1. Save the SMS in the db or our record
        Step 2. Understand the content of the message
        Step 3. Find a product match for the product ID number
        Step 4. Pass product removals off to seller_events function
        Step 5. Pass order updates off to order_events function

        Return EITHER reply message OR 200-ok OR 500-error
        On DEBUG, return error message as reply in place of 500-error
    """
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
      #msg_data is tuple of ( product_id, data{} ) or
      #just False if not understandable

      if not msg_data:#message not understandable
        #maybe they wanna chat or need help? todo:send someone an email?
        return HttpResponse(status=200)#OK

      else: #it was understandable
        (product_id, data) = msg_data
        product = Product.objects.get(id=product_id)

        product_matches_seller_phone = False #we don't know yet
        product_matches_seller_phone = product.belongsToPhone(request.POST.get('from_number'))

        if product_matches_seller_phone: #if the sender owns the product, update the order

          if data.get('remove'):
            seller_events.deactivateProduct(product)
            reply_msg = 'shukran'
          else:
            reply_msg = order_events.updateOrder(msg_data, gimme_reply_sms=True)
            #gives us reply string or True(no reply)

          if isinstance(reply_msg, basestring):
            sms.auto_reply = reply_msg
            sms.save()
            #send reply back with response
            response = {'messages':[{'content':reply_msg}]}
            return HttpResponse(json.dumps(response), mimetype='application/json')

          else:
            return HttpResponse(status=200)#OK
        else:
          return HttpResponse(status=200)#OK
          #todo: email Brahim about this incoming text product with wrong owner

    except Exception as e:
      if DEBUG:
        response = {'messages':[{'content':str(e)}]}
        return HttpResponse(json.dumps(response), mimetype='application/json')
      else:
        return HttpResponse(status=500)#server error, our fault, Telerivet will try again
        #todo: do something about it

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
    return HttpResponse(status=200)#OK
  else:
    return HttpResponse(status=403)#forbidden, didn't come from Telerivet

def understandMessage(message): #example message '1234 MAS12312938110'
  #take a message and comprehend the desired action on a product id (or return False)

  try:
    product_id = re.findall('\d+', message)[0].strip()
    product_id = Product.objects.get(id=product_id).id

  except Product.DoesNotExist: product_id = None
    #todo: email Brahim about this incoming text with wrong product id
  except: product_id = None

  if product_id:
    data = {}
    try:
      tracking_number = re.findall('[C][P]\s?\w+\s?[M][A]', message)[0]
      data['tracking_number'] = tracking_number.replace(' ','')#remove spaces
    except: pass

    #if there is an 'R' before or after a product id number
    if re.match('[rR]\s*\d+', message):
      data['remove'] = True

    return (product_id, data)
    #example ('1234', {'tracking_number':"CP123456789MA"})

  else:
    return False
