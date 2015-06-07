from django import forms

class CartForm(forms.Form):
  email       = forms.CharField(max_length=100, widget=forms.TextInput(
                  attrs={'class':"autosave required", 'placeholder':""}))
  name        = forms.CharField(max_length=100, widget=forms.TextInput(
                  attrs={'class':"autosave required", 'placeholder':""}))
  address_name= forms.CharField(max_length=100, widget=forms.TextInput(
                  attrs={'class':"autosave", 'placeholder':""}))
  address1    = forms.CharField(max_length=100, widget=forms.TextInput(
                  attrs={'class':"autosave required", 'placeholder':"address line 1"}))
  address2    = forms.CharField(max_length=100, widget=forms.TextInput(
                  attrs={'class':"autosave", 'placeholder':"address line 2"}))
  city        = forms.CharField(max_length=50,  widget=forms.TextInput(
                  attrs={'class':"autosave required", 'placeholder':"city"}))
  state       = forms.CharField(max_length=50,  widget=forms.TextInput(
                  attrs={'class':"autosave", 'placeholder':"state/region"}))
  postal_code = forms.CharField(max_length=15,  widget=forms.TextInput(
                  attrs={'class':"autosave required", 'placeholder':"zip code/post code"}))
  country     = forms.CharField(max_length=50,  widget=forms.TextInput(
                  attrs={'class':"autosave required", 'placeholder':"country"}))

class CheckoutForm(forms.Form):
  receipt     = forms.CharField(widget=forms.Textarea(
                  attrs={'placeholder': "payment data (and URL if available)",
                         'rows': "7"
                        }))
  notes       = forms.CharField(widget=forms.Textarea(
                  attrs={'placeholder': "sale details",
                         'rows': "7"
                        }))

  total_charge    = forms.DecimalField(widget=forms.TextInput())
  total_discount  = forms.DecimalField(widget=forms.TextInput())
  total_paid      = forms.DecimalField(widget=forms.TextInput())
  total_refunded  = forms.DecimalField(widget=forms.TextInput())
  currency        = forms.CharField(max_length=3, widget=forms.TextInput())