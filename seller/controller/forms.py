from django import forms

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

class SellerAssetForm(forms.ModelForm):
  class Meta:
    model = Asset
    exclude = ('seller',)

class ImageForm(forms.Form):#a form for posting directly to S3
  #action   = http://anou.s3.amazonaws.com/
  file      = forms.FileField()
  key       = forms.CharField()
  acl       = forms.CharField(default='public-read', editable=False)
  policy    = forms.CharField(default='POLICY', editable=False)
  signature = forms.CharField(defualt='SIGNATURE', editable=False)
