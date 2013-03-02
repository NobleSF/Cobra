from django import forms

class SellerEditForm(forms.Form):
  from admin.models import Country, Currency
  name      = forms.CharField()
  email     = forms.EmailField(required=False)
  #phone     = forms.CharField(widget=forms.IntegerField, required=False)
  bio       = forms.CharField(widget=forms.Textarea, required=False)
  #country   = ModelChoiceField(queryset=Country.objects.all())
  #currency  = ModelChoiceField(queryset=Currency.objects.all())
