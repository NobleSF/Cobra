import requests
from requests.auth import HTTPBasicAuth
from settings.settings import TELERIVET, STAGE, DEBUG, DEMO
import json
import re #regular expressions
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apps.admin.utils.exception_handling import ExceptionHandler
from apps.seller.models.product import Product
from apps.admin.utils.decorator import postpone
from apps.communication.controllers.email_class import Email
from settings.people import Dan, Brahim

#todo: this should be a class, not bunch of functions

def sendSMS(message, to_number, priority='1'): #using Telerivet
  try:
    post_url =  'https://api.telerivet.com/v1/projects/'
    post_url += TELERIVET['project_id'] + '/messages/outgoing'
    authentication = HTTPBasicAuth(TELERIVET['api_key'], TELERIVET['api_key'])
    parameters = {
      'phone_id':       TELERIVET['phone_id'],
      'to_number':      to_number,
      'content':        message,
      'message_type':   'sms',
      'priority':       priority,
      'status_url':     TELERIVET['status_url'],
      'status_secret':  TELERIVET['status_secret']
    }
    response = requests.post(post_url, auth=authentication, data=parameters)
    response_content = json.loads(response.content) #dict of response content

  except Exception as e:
    ExceptionHandler(e, "in sms.sendSMS-A")
    return None

  else:
    if int(response.status_code) is 200:
      return saveSMS(response_content) #responds with SMS object or exception str
    else:
      details = "status: %d" % response.status_code if response.status_code else ""
      details += ", error: %s" % response_content.get('error', 'not provided')
      e = Exception('bad request or possible Telerivet error, %s' % details)
      ExceptionHandler(e, "in sms.sendSMS-B")
      return None

@postpone #cannot return a value, handle errors internally
def sendSMSForOrder(message, to_number, order, priority='1'):
  try:
    sms = sendSMS(message, to_number, priority)
    if sms and order:
      sms.order = order
    elif sms:
      sms.save()

  except Exception as e:
    ExceptionHandler(e, "in sms.sendSMSForOrder")

def saveSMS(sms_data): #takes Telerivet response content detail at
  #https://telerivet.com/p/PJ8973e6e346c349cbcdd094fcffa9fcb5/api/rest/sending
  from apps.communication.models import SMS
  try:
    sms_messages = SMS.objects.filter(telerivet_id = sms_data['id'])
    if sms_messages:
      sms = sms_messages[0]
    else:
      sms = SMS(telerivet_id = sms_data['id'])

    if 'to_number' in sms_data:
      sms.to_number = re.sub("\D", "", sms_data['to_number'])
    else:
      sms.to_number = TELERIVET['phone_number']

    if 'from_number' in sms_data:
      sms.from_number = re.sub("\D", "", sms_data['from_number'])
    else:
      sms.from_number = TELERIVET['phone_number']

    if 'status' in sms_data:
      sms.status = sms_data['status']

    sms.message = sms_data['content']
    sms.save()

  except Exception as e:
    ExceptionHandler(e, "in sms.saveSMS")
  else:
    return sms

@csrf_exempt
def incoming(request):
  """ receives SMS messages via Telerivet, detail at
      https://telerivet.com/p/PJ8973e6e346c349cbcdd094fcffa9fcb5/api/webhook/receiving
  """
  from apps.communication.controller import order_events

  if TELERIVET['webhook_secret'] == request.POST.get('secret'):
    """
        Step 1. Save the SMS in the db or our record
        Step 2. Understand the content of the message
        Step 3. Find a product match for the product ID number
        Step 4. Handles removals
        Step 5. Pass order updates off to order_events function

        Return EITHER reply message OR 200-ok OR 500-error
        On DEBUG, return error message as reply in place of 500-error
    """
    try:
      #save the SMS in db
      sms_data = request.POST.copy()
      sms = saveSMS(sms_data)

      #who is it from?
      sender = getPhoneOwner(request.POST.get('from_number'))
      #sender is a dict of a Seller and/or/neither Artisan(asset) as {'type':object}

      #what does it say?
      msg_data = understandMessage(request.POST.get('content'))
      #msg_data is tuple of ( product_id, data{} ) or
      #just False if not understandable

      if not msg_data: #message not understood
        message = "System did not understand incoming SMS"
        message += " from %s:<br>" % request.POST.get('from_number')
        message += "%s<br>" % request.POST.get('content')
        try:
          for someone in sender:
            message += "<br>Sent by Anou %s %s." % (someone, sender[someone].name)
        except: pass
        Email(message=message).sendTo(Dan.email)
        return HttpResponse(status=200)#OK

      else: #it was understandable
        (product_id, data) = msg_data
        try:
          product = Product.objects.get(id=product_id)
        except:
          return HttpResponse(status=200)#OK

        if not product.belongsToPhone(request.POST.get('from_number')):
          message = "This SMS not from product owner: " + request.POST.get('content')
          Email(message=message).sendTo(Dan.email)
          return HttpResponse(status=200)#OK

        else:
          #if the sender owns the product, update the order

          if data.get('remove'):
            product.is_active = False
            product.save()
            reply_msg = 'shukran'
          else:
            reply_msg = order_events.updateOrder(msg_data, gimme_reply_sms=True)
            #gives us reply string or True(no reply)

          if not isinstance(reply_msg, basestring):
            return HttpResponse(status=200)#OK
          else:
            sms.auto_reply = reply_msg
            sms.save()
            #send reply back with response
            response = {'messages':[{'content':reply_msg}]}
            return HttpResponse(json.dumps(response), content_type='application/json')

          #todo: email Brahim about this incoming text product with wrong owner

    except Exception as e:
      ExceptionHandler(e, "in sms.incoming")

      if DEMO or STAGE or DEBUG:
        response = {'messages':[{'content':str(e)}]}
        return HttpResponse(json.dumps(response), content_type='application/json')
      else:
        return HttpResponse(status=500)#server error, our fault, Telerivet will try again

  else:
    return HttpResponse(status=403)#forbidden, didn't come from Telerivet

@csrf_exempt
def status_confirmation(request):
  #confirming that a sent SMS successfully reached it's recipient, detail at
  #https://telerivet.com/p/PJ8973e6e346c349cbcdd094fcffa9fcb5/api/webhook/status

  #if not POST did not come from Telerivet
  try:
    if request.POST['secret'] == TELERIVET['status_secret']:
      data = request.POST.copy() #dict of response content
      saveSMS(data)
      return HttpResponse(status=200)#OK
    else:
      raise Exception

  except:
    return HttpResponse(status=403)#forbidden, didn't come from Telerivet

def getPhoneOwner(phone_number):
  from apps.seller.models.seller import Seller
  from apps.seller.models.asset import Asset

  phone_number = phone_number[-8:]
  sender = {}
  try: sender['Seller'] = Seller.objects.get(account__phone__endswith=phone_number)
  except: pass
  try: sender['Artisan'] = Assets.objects.filter(phone__endswith=phone_number)[0]
  except: pass
  return sender

def understandMessage(message): #example message '123 CP123456789MA'
  #take a message and comprehend the desired action on a product id (or return False)

  try: #find the product id
    #remove leading and trailing whitespace and upper-case all letters
    message = message.strip().upper()

    # regex pattern ^\D{0,2}(\d{1,4})(?![\d])
    #up to 2 non-digits from start of string,
    #then product ID 1-4 digits length (captured)
    #followed by anything but another digit

    pattern = re.compile('^\D{0,2}(\d{1,4})(?![\d])')
    matches = pattern.match(message)
    product_id = matches.group(1) #captured product_id
    product = Product.objects.get(id=product_id)
  except:
    product = None

  stripped_message = re.sub(r'\W', '', message) #strip out all whitespace

  if product and stripped_message == str(product.id): #only product id
    return (product.id, {})

  elif product:
    """ systematically check each possible command/action on the product id
        1. remove action
        2. tracking number assignment
    """
    data = {}

    try: #check for product remove command "R123"
      #regex looks for R or X before or after product id
      pattern = re.compile('^([RX])?(\d{1,4})([RX])?$')
      matches = pattern.match(stripped_message)

      #if only one match exists, one had to have been an X or R
      if bool(matches.group(1)) != bool(matches.group(3)):
        data['remove'] = True
    except: pass

    try: #check for tracking number
      #regex looks for 2 letters, 6-12 digits, followed by 'MA'
      pattern = re.compile('\S*([A-Z]{2}\d{6,12}[M][A])\S*')
      matches = pattern.match(stripped_message)
      data['tracking_number'] = matches.group(1)
    except: pass

    return (product.id, data) #like ('1234', {'tracking_number':"CP123456789MA"})

  else:
    return False
