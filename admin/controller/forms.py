from django.db import models
from django import forms
from admin.models import Account
from admin.controller.account import process_password

class AccountCreateForm(forms.ModelForm):
  #username  = forms.EmailField(label="Email")
  #password  = forms.CharField(widget=forms.PasswordInput)
  #public_key  = forms.CharField(widget=forms.HiddenInput, required=False)
  class Meta:
    model = Account

  def clean_password(self):
    return process_password(cleaned_data['password'])


class AccountEditForm(forms.ModelForm):
  class Meta:
    model = Account

  def clean_password(self):
    return process_password(cleaned_data['password'])


class AccountLoginForm(forms.ModelForm):
  #public_key  = forms.CharField(widget=forms.HiddenInput, required=False)
  class Meta:
    model = Account
    fields = {'username', 'password'}

  def clean_password(self):
    return process_password(cleaned_data['password'])

class AccountPasswordForm(forms.Form):
  old_password  = forms.CharField(widget=forms.PasswordInput)
  new_password  = forms.CharField(widget=forms.PasswordInput)
  #public_key  = forms.CharField(widget=forms.HiddenInput, required=False)

  def clean_old_password(self):
    return process_password(cleaned_data['_old_password'])
  def clean_new_password(self):
    return process_password(cleaned_data['new_password'])
