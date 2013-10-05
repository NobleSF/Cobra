from apps.communication import models
from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from settings.settings import STAGE, DEBUG, DEMO
from apps.admin.controller.decorator import postpone

class Email(object):
  def __init__(self, template_dir=None, data={}, message=None):
    #creates an email using the template and data provided
    if template_dir:

      subject_template = "email/%s/subject.txt" % template_dir
      text_body_template = "email/%s/text_body.txt" % template_dir
      html_body_template = "email/%s/html_body.html" % template_dir

      #plaintext_context = Context(autoescape=False)
      context = {'data':data}

      self.subject = render_to_string(subject_template, context)
      self.text_body = render_to_string(text_body_template, context)
      self.html_body = render_to_string(html_body_template, context)

      #default from address
      self.from_email = "Anou <hello@theanou.com>"

    else:
      message = str(message) if message else 'test email body'
      self.subject = 'notification'
      self.text_body = message
      self.html_body = '<p>%s</p>' % message
      self.from_email = 'system@theanou.com'

  def sendFrom(self, from_email):
    self.from_email = from_email
    return self

  @postpone #cannot return a value, handle errors internally
  def sendTo(self, to): #sends the email object to the provided email or list of emails

    #allow the function to receive a string or a list
    self.to = [to] if isinstance(to, basestring) else to

    if STAGE or DEBUG or DEMO: #redirect non-production emails
      if DEMO:
        server_name = 'DEMO'
        self.from_email = "demo@theanou.com"
      elif STAGE:
        server_name = 'STAGE'
        self.from_email = "stage@theanou.com"
      else:
        server_name = 'LOCAL'
        self.from_email = "local@theanou.com"

      self.text_body = "*%s* To: %s\n %s" % (server_name,
                                             ','.join(self.to),
                                             self.text_body)
      self.html_body = "<h2>*%s* To: %s</h2> %s" % (server_name,
                                                    ','.join(self.to),
                                                    self.html_body)
      self.to = [('dev+test-%s@theanou.com' % server_name)]

    try:
      self.mail = EmailMultiAlternatives(
                    subject     = self.subject,
                    body        = self.text_body,
                    from_email  = self.from_email,
                    to          = self.to
                  )
      #sendgrid settings automatically bcc dump@theanou.com on every email
      self.mail.attach_alternative(self.html_body, "text/html")
      self.mail.send()
      save_response = self.save()

      if isinstance(save_response, basestring):
        error_message = save_response

    except Exception as e:
      error_message = "Error in communcation/controller/email_class.py sendTo(): " + str(e)

    try:
      if error_message:
        from settings.people import Tom
        Email(message=error_message).sendTo(Tom.email)
    except Exception as e2:
      try:
        if error_message:
          from apps.communication.controller.sms import sendSMS
          from settings.people import Tom
          sendSMS("THE SKY IS FALLING! \r\n in email_class sendTo()", Tom.phone)
      except: pass #resistance is futile

  def save(self):
    try:    self.order
    except: self.order = None

    try:
      email = models.Email(
                from_address  = self.mail.from_email,
                to_address    = ','.join(self.mail.to),
                subject       = self.mail.subject,
                text_body     = self.mail.body,
                html_body     = self.mail.alternatives[0][0],
                order         = self.order
              )
    except Exception as e:
      return "error: " + str(e)
    else:
      email.save()
      return True

  def assignToOrder(self, order):
    self.order = order
