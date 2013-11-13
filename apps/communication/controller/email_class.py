from apps.communication import models
from apps.admin.utils.exception_handling import ExceptionHandler
from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from settings.settings import STAGE, DEBUG, DEMO
from apps.admin.utils.decorator import postpone

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
      self.save()

    except Exception as e:
      ExceptionHandler(e, "in email_class.sendTo", sentry_only=True)

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
      ExceptionHandler(e, "in email_class.save")
    else:
      email.save()

  def assignToOrder(self, order):
    self.order = order
