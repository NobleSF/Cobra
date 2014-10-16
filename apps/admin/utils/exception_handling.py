from apps.admin.utils.decorator import postpone
from settings import people

class ExceptionHandler(object):
  """
  A plethora of options for handling exceptions
  and other mischievous activities that should be reported
  """
  def __init__(self, exception, message=None,
               sentry_only=False, tom_only=False, #todo: replace sentry_only with no_email
               sos_sms=False):
    self.exception = exception
    self.message = message

    if sentry_only: self.tellSentry()
    elif tom_only: self.emailTom()

    else:
      self.tellSentry()
      self.emailTom()

    if sos_sms:
      self.smsTom(sos=True)
      self.smsDan(sos=True)

  @postpone
  def tellSentry(self):
    from settings.settings import PRODUCTION
    if PRODUCTION:
      from raven.contrib.django.models import client as Sentry
      try:
        raise self.exception
      except:
        Sentry.captureException()
    else:
      pass

  #email is already async, no need for @postpone
  def emailTom(self):
    from apps.communication.controllers.email_class import Email
    try:
      message = self.message if self.message else "Something broke."
      message += "<br>%s" % str(self.exception)
      Email(message=message).sendTo([person.email for person in people.developer_team])
    except Exception as e:
      ExceptionHandler(e, sentry_only=True)
      self.smsTom(sos=True)

  @postpone
  def smsTom(self, sos=False):
    from apps.communication.controllers.sms import sendSMS
    message  = "ANOU SAYS: THERE'S SNOW IN IMOUZZER\r\n" if sos else ""
    message += ("%s" % self.message) if self.message else ""
    message += "\r\n%s" % str(self.exception)
    sendSMS(message, people.Tom.phone)

  @postpone
  def smsDan(self, sos=False):
    from apps.communication.controllers.sms import sendSMS
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
