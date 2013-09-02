import requests
from requests.auth import HTTPBasicAuth
from settings.settings import TELERIVET, STAGE, DEBUG
import simplejson as json
import re #regular expressions
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apps.communication.models import SMS
from apps.seller.models import Product
from apps.admin.controller.decorator import postpone
from apps.communication.controller.email_class import Email
from settings.people import Tom

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
    return "send error: " + str(e)

  else:
    if int(response.status_code) is 200:
      return saveSMS(response_content) #responds with SMS object or exception str
    else:
      return "bad request or possible Telerivet error"

@postpone #cannot return a value, handle errors internally
def sendSMSForOrder(message, to_number, order, priority='1'):
  try:
    sms = sendSMS(message, to_number, priority)
    if isinstance(sms, SMS):
      sms.order = order
      sms.save()
    else:
      error_message = sms
  except Exception as e:
    error_message = "Error in communcation/controller/sms.py saveSMS(): " + str(e)

  try:
    if error_message:
      Email(message=error_message).sendTo(Tom.email)
  except: pass

def saveSMS(sms_data): #takes Telerivet response content detail at
  #https://telerivet.com/p/PJ8973e6e346c349cbcdd094fcffa9fcb5/api/rest/sending
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
    return "save error: " + str(e)
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
      data = request.POST.copy()
      sms = saveSMS(data)

      #look at what we received
      msg_data = understandMessage(request.POST['content'])
      #msg_data is tuple of ( product_id, data{} ) or
      #just False if not understandable

      if not msg_data:#message not understandable
        #maybe they wanna chat or need help? todo:send someone an email?
        return HttpResponse("hello?", status=200)#OK

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
      if STAGE or DEBUG:
        response = {'messages':[{'content':str(e)}]}
        return HttpResponse(json.dumps(response), mimetype='application/json')
      else:
        error_message = "error on incoming SMS: " +  str(e)
        Email(message=error_message).sendTo(Tom.email)
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

  except Product.DoesNotExist:
    product_id = None
    #todo: email Brahim about this incoming text with wrong product id
  except:
    product_id = None

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
