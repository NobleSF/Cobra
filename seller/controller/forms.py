from django import forms

class SellerForm(forms.Form):
  #from admin.models import Country, Currency
  name      = forms.CharField()
  email     = forms.EmailField(required=False)
  phone     = forms.IntegerField()
  bio       = forms.Textarea(required=False)
  #country   = ModelChoiceField(queryset=Country.objects.all())
  #currency  = ModelChoiceField(queryset=Currency.objects.all())
