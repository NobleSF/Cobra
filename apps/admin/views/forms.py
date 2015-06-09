from django import forms
from django.forms.widgets import TextInput
from apps.admin.models.account import Account
from apps.admin.views.account import processPassword


class NumberInput(TextInput):
  input_type = 'tel'

class AccountCreateForm(forms.Form):
  name          = forms.CharField(max_length=50, required=False)
  phone         = forms.CharField(widget=NumberInput(), max_length=15)
  password      = forms.CharField(widget=NumberInput(), max_length=100)

  def clean_password(self):
    return processPassword(self.cleaned_data['password'])

class AccountEditForm(forms.ModelForm):
  class Meta:
    model = Account
    exclude = ['password','admin_type']

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
    return processPassword(self.cleaned_data['password'])

class AccountPasswordForm(forms.Form):
  new_password  = forms.CharField(widget=NumberInput(attrs={'autocomplete':'off'}))

class SMSForm(forms.Form):
  to_number     = forms.CharField(widget=NumberInput(
                          attrs={'placeholder':''}))
  message       = forms.CharField(widget=forms.Textarea(
                          attrs={'placeholder':'...'}))
  order         = forms.CharField(widget=forms.TextInput(
                          attrs={'placeholder':''}))
