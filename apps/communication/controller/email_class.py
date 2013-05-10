from apps.communtication import models
from django.template.loader import render_to_string

class Email:
  def __init__(self, template_name):
    self.template_name = template_name




  def object(self, cart=None, order=None, event=None):
    if cart:
      self.data = dict(cart)
      self.category = 'cart'
    elif order:
      self.data = dict(order)
      self.category = 'order'
    else:
      self.data = dict()
      self.category = 'dunno'

  def action(self, template_name):
    from django.template import context

    file_location = "email/" + self.category + "/" + template_name + "/"
    subject_template = file_location + "subject.txt"
    text_body_template = file_location + "text_body.txt"
    html_body_template = file_location + "html_body.html"

    plaintext_context = Context(autoescape=False) #HTML escaping not appropriate in plaintext
    self.subject = render_to_string(subject_template, self.data, plaintext_context)
    self.text_body = render_to_string(text_body_template, self.data, plaintext_context)
    self.html_body = render_to_string(html_body_template, self.data, plaintext_context)

  def send():
    from django.core.mail import EmailMultiAlternatives
    self.mail = EmailMultiAlternatives(
                  subject     = self.subject,
                  from_email  = "hello@theanou.com",
                  to          = ["test@theanou.com"],
                  body        = self.text_body
                )
    self.mail.attach_alternative(self.html_body, "text/html")
    self.save()
    self.mail.send()
    #if error:
      #report error, or save to variable in Email db model object

  def save(self):
    email = models.Email(
      from_address  = self.mail.from_email,
      to_address    = self.mail.to[0],
      subject       = self.mail.subject,
      html_body     = self.mail.body,
      text_boby     = self.mail.alternatives[0][0]
    )
    cart.save()
    request.session['cart_id'] = cart.id
    return cart
