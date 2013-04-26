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
  image_url   = forms.CharField(
                  widget=forms.TextInput(
                    attrs={'class':"image-url autosave", 'data-asset_id':""}))
                  #image takes url of image after ajax upload to cloudinary
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

class ImageForm(forms.Form):
  from anou.settings import CLOUDINARY

  timestamp       = forms.CharField(label="", initial="not yet set")
  signature       = forms.CharField(label="", initial="not yet set")
  api_key         = forms.CharField(label="", initial=CLOUDINARY['api_key'])

  format          = forms.CharField(label="", initial=CLOUDINARY['format'])
  transformation  = forms.CharField(label="", initial=CLOUDINARY['transformation'])
  tags            = forms.CharField(label="")

  file            = forms.FileField(label="",
                      widget=forms.FileInput(attrs={  'class':'image-input',
                                                      'accept':'*',
                                                      'capture':'camera'
                                                    })
                    )

class PhotoForm(forms.Form):
  from anou.settings import CLOUDINARY

  timestamp       = forms.CharField(label="", initial="not yet set")
  signature       = forms.CharField(label="", initial="not yet set")
  api_key         = forms.CharField(label="", initial=CLOUDINARY['api_key'])

  format          = forms.CharField(label="", initial=CLOUDINARY['format'])
  transformation  = forms.CharField(label="", initial=CLOUDINARY['transformation'])
  tags            = forms.CharField(label="")

  file            = forms.FileField(label="",
                      widget=forms.FileInput(attrs={  'class':'photo-input',
                                                      'accept':'*',
                                                      'capture':'camera'
                                                    })
                    )
  product         = forms.CharField(label="")
  rank            = forms.CharField(label="")

class ProductEditForm(forms.Form):
  product_id        = forms.CharField(
                        widget=forms.TextInput(),
                        initial="none")

  assets            = forms.CharField(
                        widget=forms.TextInput(),
                        initial=" ")
  shipping_options  = forms.CharField(
                        widget=forms.TextInput(),
                        initial=" ")
  colors            = forms.CharField(
                        widget=forms.TextInput(),
                        initial=" ")

  photos            = forms.CharField(
                        widget=forms.TextInput())

  price             = forms.CharField(
                        widget=forms.TextInput(attrs={'class':"autosave giveMeData"}))
  length            = forms.CharField(
                        widget=forms.TextInput(attrs={'class':"autosave giveMeData"}))
  width             = forms.CharField(
                        widget=forms.TextInput(attrs={'class':"autosave giveMeData"}))
  height            = forms.CharField(
                        widget=forms.TextInput(attrs={'class':"autosave giveMeData"}))
  weight            = forms.CharField(
                        widget=forms.TextInput(attrs={'class':"autosave giveMeData"}))
