from django.db import models
from django import forms
from admin.models import Account

class AccountCreateForm(forms.Form):
  username  = forms.EmailField(label="Email")
  password  = forms.CharField(widget=forms.PasswordInput)
  #public_key  = forms.CharField(widget=forms.HiddenInput, required=False)

class AccountEditForm(forms.ModelForm):
  class Meta:
    model = Account

class AccountLoginForm(forms.Form):
  username    = forms.EmailField(label="Email")
  password    = forms.CharField(widget=forms.PasswordInput)
  #public_key  = forms.CharField(widget=forms.HiddenInput, required=False)

class AccountPasswordForm(forms.Form):
  old_password  = forms.CharField(widget=forms.PasswordInput)
  new_password  = forms.CharField(widget=forms.PasswordInput)
  #public_key  = forms.CharField(widget=forms.HiddenInput, required=False)
