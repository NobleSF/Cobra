from django import forms

class AccountCreateForm(forms.Form):
  username  = forms.EmailField(label="Email")
  password  = forms.CharField(widget=forms.PasswordInput)
  #public_key  = forms.CharField(widget=forms.HiddenInput, required=False)

class AccountLoginForm(forms.Form):
  username    = forms.EmailField(label="Email")
  password    = forms.CharField(widget=forms.PasswordInput)
  #public_key  = forms.CharField(widget=forms.HiddenInput, required=False)

class AccountPasswordForm(forms.Form):
  old_password  = forms.CharField(widget=forms.PasswordInput)
  new_password  = forms.CharField(widget=forms.PasswordInput)
  #public_key  = forms.CharField(widget=forms.HiddenInput, required=False)
