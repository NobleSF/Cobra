from django.db import models
from django import forms
from apps.admin.models import Account
from apps.admin.controller.account import process_password

from django.forms.widgets import TextInput
class NumberInput(TextInput):
  input_type = 'tel'

class AccountCreateForm(forms.Form):
  username      = forms.CharField(max_length=100)
  password      = forms.CharField(max_length=100)
  account_type  = forms.MultipleChoiceField(
                    widget=forms.Select,
                    choices=(('seller','seller'),('admin','admin'))
                  )

  def clean_password(self):
    return process_password(self.cleaned_data['password'])

class AccountEditForm(forms.ModelForm):
  class Meta:
    model = Account
    exclude = ['password','is_admin']

  def clean_phone(self):
    data = str(self.cleaned_data['phone'])

    #must be blank or number
    if data and not data.isdigit():
      raise forms.ValidationError("Phone must be a number.")

    #must be blank or 8 or more characters
    if data and len(data) < 8:
      raise forms.ValidationError("Phone must be at least 8 digits.")

    #must not have the same ending 8 characters as any other phone
    if len(Account.objects.filter(phone__endswith=data[-8:])) > 1:
      raise forms.ValidationError("Account with this Phone already exists.")

    return data

  def clean_username(self):
    data = str(self.cleaned_data['username'])

    #must not begin with a digit
    if data[0].isdigit():
      raise forms.ValidationError("Username must not begin with a number.")

    #must not end with 8 digits
    if data[-8:].isdigit():
      raise forms.ValidationError("Username may not end with those numbers.")

    #must not have @ in it
    if data.find("@") > -1:
      raise forms.ValidationError("Username may not contain @ symbol.")

    return data


class AccountLoginForm(forms.Form):
  username  = forms.CharField(widget=NumberInput())
  password  = forms.CharField(widget=NumberInput(attrs={'autocomplete':'off'}))

  def clean_password(self):
    return process_password(self.cleaned_data['password'])

class AccountPasswordForm(forms.Form):
  new_password  = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off'}))

class SMSForm(forms.Form):
  to_number     = forms.CharField(widget=NumberInput(
                          attrs={'placeholder':'phone #'}))
  message       = forms.CharField(widget=forms.Textarea(
                          attrs={'placeholder':'message'}))
  order         = forms.CharField(widget=forms.TextInput(
                          attrs={'placeholder':'order #'}))
