from django.db import models
from django import forms
from apps.admin.models import Account
from apps.admin.controller.account import process_password

from django.forms.widgets import TextInput
class NumberInput(TextInput):
  input_type = 'tel'

class AccountCreateForm(forms.ModelForm):
  is_seller = forms.BooleanField(label='Seller', required=False)
  public_key  = forms.CharField(label='', widget=forms.HiddenInput, required=False)
  class Meta:
    model = Account

  def clean_password(self):
    return process_password(self.cleaned_data['password'])
  def clean_email(self):
      email = self.cleaned_data['email']
      if email == '': email = None
      return email

class AccountEditForm(forms.ModelForm):
  class Meta:
    model = Account

  def clean_password(self):
    return process_password(self.cleaned_data['password'])


class AccountLoginForm(forms.Form):
  username  = forms.CharField(widget=NumberInput(attrs={'autofocus':''}))
  password  = forms.CharField(widget=NumberInput())

  def clean_password(self):
    return process_password(self.cleaned_data['password'])

class AccountPasswordForm(forms.Form):
  old_password  = forms.CharField(widget=forms.PasswordInput)
  new_password  = forms.CharField(widget=forms.PasswordInput)
  #public_key  = forms.CharField(widget=forms.HiddenInput, required=False)

  def clean_old_password(self):
    return process_password(self.cleaned_data['old_password'])
  def clean_new_password(self):
    return process_password(self.cleaned_data['new_password'])
