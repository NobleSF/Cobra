from django import forms
from apps.public.models import Cart
from django import forms

class CartForm(forms.Form):
  email       = forms.CharField(max_length=100, widget=forms.TextInput(
                  attrs={'class':"autosave required", 'placeholder':"email address"}))
  name        = forms.CharField(max_length=100, widget=forms.TextInput(
                  attrs={'class':"autosave required", 'placeholder':"your name"}))

class ManualCheckoutForm(forms.Form):
  #SHIPPING ADDRESS
  address1    = forms.CharField(max_length=100, widget=forms.TextInput(
                  attrs={'class':"autosave required", 'placeholder':"address line 1"}))
  address2    = forms.CharField(max_length=100, widget=forms.TextInput(
                  attrs={'class':"autosave", 'placeholder':"address line 2"}))
  city        = forms.CharField(max_length=50,  widget=forms.TextInput(
                  attrs={'class':"autosave required", 'placeholder':"city"}))
  state       = forms.CharField(max_length=50,  widget=forms.TextInput(
                  attrs={'class':"autosave required", 'placeholder':"state/region"}))
  postal_code = forms.CharField(max_length=15,  widget=forms.TextInput(
                  attrs={'class':"autosave required", 'placeholder':"zip code/post code"}))
  country     = forms.CharField(max_length=50,  widget=forms.TextInput(
                  attrs={'class':"autosave required", 'placeholder':"country"}))

  #ORDER DETAILS
  receipt     = forms.CharField(widget=forms.Textarea(
                  attrs={'class':"autosave required",
                         'placeholder':"payment data (and URL if available)",
                         'rows':"7"
                        }))
  notes       = forms.CharField(widget=forms.Textarea(
                  attrs={'class':"autosave required",
                         'placeholder':"sale details (and URL if available)",
                         'rows':"7"
                        }))
