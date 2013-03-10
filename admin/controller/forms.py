from django.db import models
from django import forms
from admin.models import Account

class AccountCreateForm(forms.ModelForm):
  #username  = forms.EmailField(label="Email")
  #password  = forms.CharField(widget=forms.PasswordInput)
  #public_key  = forms.CharField(widget=forms.HiddenInput, required=False)
  class Meta:
    model = Account

  #after validation, decrypt with private key
  #hash the password

class AccountEditForm(forms.ModelForm):
  class Meta:
    model = Account

class AccountLoginForm(forms.ModelForm):
  #public_key  = forms.CharField(widget=forms.HiddenInput, required=False)
  class Meta:
    model = Account
    fields = {'username', 'password'}

class AccountPasswordForm(forms.Form):
  old_password  = forms.CharField(widget=forms.PasswordInput)
  new_password  = forms.CharField(widget=forms.PasswordInput)
  #public_key  = forms.CharField(widget=forms.HiddenInput, required=False)
