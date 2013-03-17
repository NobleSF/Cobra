from django.db import models
from django import forms
from seller.models import Asset, Product, Seller

class SellerEditForm(forms.Form):
  from admin.models import Country, Currency
  name      = forms.CharField()
  email     = forms.EmailField(required=False)
  phone     = forms.CharField(required=False)
  bio       = forms.CharField(widget=forms.Textarea, required=False)
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

class AssetProductForm(forms.Form):
  ilk         = forms.HiddenInput(value='product')
  image       = forms.HiddenInput()#stores the id of the uploaded image
  name        = forms.CharField(max_length=50, required=False)
  description = forms.Textarea(required=False)
  category    = forms.SelectMultiple(required=False,
                                      choices=Category.objects.all()#category model
                                    )

class AssetArtisanForm(forms.Form):
  ilk         = forms.HiddenInput(value='artisan')
  image       = forms.HiddenInput()#stores the id of the uploaded image
  name        = forms.CharField(max_length=50, required=False)
  description = forms.Textarea(required=False)

class AssetToolForm(forms.Form):
  ilk         = forms.HiddenInput(value='tool')
  image       = forms.HiddenInput()#stores the id of the uploaded image
  name        = forms.CharField(max_length=50, required=False)
  description = forms.Textarea(required=False)

class AssetMaterialForm(forms.Form):
  ilk         = forms.HiddenInput(value='material')
  image       = forms.HiddenInput()#stores the id of the uploaded image
  name        = forms.CharField(max_length=50, required=False)
  description = forms.Textarea(required=False)

#attempt at a generic Asset Form
class AssetForm(forms.Form, ilk):
  ilk         = forms.HiddenInput(value=ilk)
  image       = forms.HiddenInput()#stores the id of the uploaded image
  name        = forms.CharField(max_length=50, required=False)
  description = forms.Textarea(required=False)
  if ilk == 'product':
    category  = forms.SelectMultiple(required=False,
                                      choices=Category.objects.all()#category model
                                    )

class ImageForm(forms.Form):#a form for posting directly to S3
  action      = "http://anou.s3.amazonaws.com/"
  file        = forms.FileField()
  key         = forms.CharField()
  #acl        = forms.CharField(type='hidden', default='public-read', editable=False)
  #policy     = forms.CharField(default='POLICY', editable=False)
  #signature  = forms.CharField(default='SIGNATURE', editable=False)
