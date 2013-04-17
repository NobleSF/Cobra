from django.db import models
from django import forms
from seller.models import Asset, Product, Seller, Image, Photo
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
    import re #regular expressions
    phone = self.cleaned_data['phone']
    #require country calling code
    phone = re.sub('\D', '', phone)
    if 10 <= len(phone) <= 14:
      return phone
    elif len(phone) == 0:
      return None
    else:
      raise forms.ValidationError("number of digits incorrect")

class AssetForm(forms.Form):
  asset_id    = forms.CharField(
                  widget=forms.TextInput(attrs={'class':"asset-id"}), initial="none")

  ilk         = forms.CharField(
                  widget=forms.TextInput(attrs={'class':"ilk"}))
  image       = forms.CharField(
                  widget=forms.TextInput(
                    attrs={'class':"image-id autosave", 'data-asset_id':""}))
                  #image takes id of image after ajax upload
  DELETE      = forms.BooleanField(
                  widget=forms.CheckboxInput(
                    attrs={'class':"delete autosave", 'data-asset_id':""}))

  name        = forms.CharField(
                  widget=forms.TextInput(
                    attrs={'class':"name autosave", 'data-asset_id':""}),
                    max_length=50, required=False)
  description = forms.CharField(
                  widget=forms.Textarea(
                    attrs={'class':"description autosave", 'data-asset_id':""}),
                    required=False)
  category    = forms.ModelMultipleChoiceField(
                  widget=forms.SelectMultiple(
                    attrs={'class':"category autosave", 'data-asset_id':""}),
                    queryset=Category.objects.all())

class ImageForm(forms.ModelForm):
  class Meta:
    model = Image
    fields = ('original',)
    widgets = {
      'original': forms.FileInput(attrs={'class':'image-input',
                                         'accept':'image/*',
                                         'capture':'camera'})
    }

class PhotoForm(forms.ModelForm):
  class Meta:
    model = Photo
    fields = ('product','rank','original',)
    widgets = {
      'product':  forms.TextInput(attrs=None),
      'rank':     forms.TextInput(attrs=None),
      'original': forms.FileInput(attrs={'class':'image-input',
                                         'accept':'image/*',
                                         'capture':'camera'})
    }

class ProductEditForm(forms.Form):
  product_id      = forms.CharField(
                      widget=forms.TextInput(attrs={'id':"product-id"}),
                      initial="none")

  assets          = forms.CharField(
                      widget=forms.TextInput(attrs={'id':"assets"}))
  images          = forms.CharField(
                      widget=forms.TextInput(attrs={'id':"images"}))
  shipping_option = forms.CharField(
                      widget=forms.TextInput(attrs={'id':"shipping-option"}))

  color           = forms.CharField(
                      widget=forms.TextInput(attrs={'id':"color"}))
  width           = forms.CharField(
                      widget=forms.TextInput(attrs={'id':"width"}))
  height          = forms.CharField(
                      widget=forms.TextInput(attrs={'id':"height"}))
  length          = forms.CharField(
                      widget=forms.TextInput(attrs={'id':"length"}))
  weight          = forms.CharField(
                      widget=forms.TextInput(attrs={'id':"weight"}))
  price           = forms.CharField(
                      widget=forms.TextInput(attrs={'id':"price"}))
