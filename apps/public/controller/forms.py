from django import forms
from apps.public.models import Cart
from django import forms

class CartForm(forms.Form):
  email       = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':"autosave"}))
  name        = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':"autosave"}))
  address1    = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':"autosave"}))
  address2    = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':"autosave"}))
  city        = forms.CharField(max_length=50,  widget=forms.TextInput(attrs={'class':"autosave"}))
  state       = forms.CharField(max_length=50,  widget=forms.TextInput(attrs={'class':"autosave"}))
  postal_code = forms.CharField(max_length=15,  widget=forms.TextInput(attrs={'class':"autosave"}))
  country     = forms.CharField(max_length=50,  widget=forms.TextInput(attrs={'class':"autosave"}))
