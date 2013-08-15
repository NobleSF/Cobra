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
                    choices=(('admin','admin'),('seller','seller'))
                  )

  def clean_password(self):
    return process_password(self.cleaned_data['password'])

class AccountEditForm(forms.ModelForm):
  class Meta:
    model = Account
    exclude = ['password','is_admin']

  def clean_password(self):
    return process_password(self.cleaned_data['password'])


class AccountLoginForm(forms.Form):
  username  = forms.CharField(widget=NumberInput())
  password  = forms.CharField(widget=NumberInput(attrs={'autocomplete':'off'}))

  def clean_password(self):
    return process_password(self.cleaned_data['password'])

class AccountPasswordForm(forms.Form):
  old_password  = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'off'}))
  new_password  = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'off'}))
  #public_key  = forms.CharField(widget=forms.HiddenInput, required=False)

  def clean_old_password(self):
    return process_password(self.cleaned_data['old_password'])
  def clean_new_password(self):
    return process_password(self.cleaned_data['new_password'])

class SMSForm(forms.Form):
  to_number     = forms.CharField(widget=NumberInput())
  message       = forms.CharField(widget=forms.Textarea)
