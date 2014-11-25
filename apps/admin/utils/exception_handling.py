from apps.admin.utils.decorator import postpone
from settings import people
import rollbar
from settings.settings import DEBUG, LOCAL


class ExceptionHandler(object):
  """
  A plethora of options for handling exceptions
  and other mischievous activities that should be reported
  """
  def __init__(self, exception, message=None,
               no_email=False, tom_only=False,
               sos_sms=False):
    self.exception = exception
    self.message = message

    if DEBUG:
      print message, str(exception)
      no_email = True if LOCAL else no_email

    if no_email:
      self.reportIt()
    elif tom_only:
      self.emailTom()
    else:
      self.reportIt()
      self.emailTom()

    if sos_sms:
      self.smsTom(sos=True)
      self.smsDan(sos=True)

  @postpone
  def reportIt(self):
    try:
      raise self.exception
    except:
      rollbar.report_exc_info()
      # if we had the request object
      #rollbar.report_exc_info(request=request)
      # additional params
      #rollbar.report_exc_info(request=request, extra_data={'bar': bar})


  #email is already async, no need for @postpone
  def emailTom(self):
    from apps.communication.controller.email_class import Email
    try:
      message = self.message if self.message else "Something broke."
      message += "<br>%s" % str(self.exception)
      Email(message=message).sendTo([person.email for person in people.developer_team])
    except Exception as e:
      ExceptionHandler(e, no_email=True)
      self.smsTom(sos=True)

  @postpone
  def smsTom(self, sos=False):
    from apps.communication.controller.sms import sendSMS
    message  = "ANOU SAYS: THERE'S SNOW IN IMOUZZER\r\n" if sos else ""
    message += ("%s" % self.message) if self.message else ""
    message += "\r\n%s" % str(self.exception)
    sendSMS(message, people.Tom.phone)

  @postpone
  def smsDan(self, sos=False):
    from apps.communication.controller.sms import sendSMS
    message  = "ANOU SAYS: THERE'S SNOW IN IMOUZZER\r\n" if sos else ""
    message += ("%s" % self.message) if self.message else ""
    sendSMS(message, people.Dan.phone)

"""
example usage:

from apps.admin.utils.exception_handling import ExceptionHandler
try:
  1/0
except:
  ExceptionHandler(e,"optional message")
"""
