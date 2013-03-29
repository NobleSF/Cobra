from django.db import models
from django import forms
from seller.models import Asset, Product, Seller, Image
from admin.models import Category

class SellerEditForm(forms.Form):
  from admin.models import Country, Currency
  name      = forms.CharField()
  email     = forms.EmailField(required=False)
  phone     = forms.CharField(required=False)
  bio       = forms.CharField(widget=forms.Textarea(attrs={'class':"description"}),
                              required=False)
  country   = forms.ModelChoiceField(queryset=Country.objects.all())
  currency  = forms.ModelChoiceField(queryset=Currency.objects.all())

  def clean_phone(self):
    phone = self.cleaned_data['phone']
    #require country code
    phone = phone.translate(None, string.digits)
    if 10 <= len(phone) <= 14:
      return phone
    else:
      return error

class AssetForm(forms.Form):
  ilk         = forms.CharField(
                  widget=forms.TextInput(attrs={'class':"ilk"}))
  image       = forms.CharField(
                  widget=forms.TextInput(attrs={'class':"image-key"}))
                  #image takes id of image after ajax upload
  name        = forms.CharField(
                  widget=forms.TextInput(attrs={'class':"name"}),
                  max_length=50, required=False)
  description = forms.CharField(
                  widget=forms.Textarea(attrs={'class':"description"}),
                  required=False)
  category    = forms.ModelMultipleChoiceField(
                  widget=forms.SelectMultiple(attrs={'class':"category"}),
                  queryset=Category.objects.all())
  DELETE      = forms.BooleanField(
                  widget=forms.CheckboxInput())

class ImageForm(forms.ModelForm):

  class Meta:
    model = Image
    fields = ('original',)
    widgets = {
      'original': forms.FileInput(attrs={'class':'image-input',
                                         'accept':'image/*',
                                         'capture':'camera'})
    }
