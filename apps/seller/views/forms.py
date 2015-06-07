from django import forms
from django.forms.widgets import TextInput
from apps.admin.models.category import Category

class NumberInput(TextInput):
  input_type = 'tel'

class SellerEditForm(forms.Form):
  from apps.admin.models.country import Country

  name          = forms.CharField(required=False)
  email         = forms.EmailField(required=False)
  phone         = forms.CharField(widget=NumberInput(), required=False)

  bank_name     = forms.CharField(required=False)
  bank_account  = forms.CharField(required=False)

  bio           = forms.CharField(
                    widget=forms.Textarea(attrs={'class':"description"}),
                      required=False)
  bio_ol        = forms.CharField(
                    widget=forms.Textarea(attrs={'class':"description"}),
                      required=False)

  city          = forms.CharField(required=False)
  country       = forms.ModelChoiceField(queryset=Country.objects.all())
  coordinates   = forms.CharField(required=False)

  def clean_phone(self):
    import re #regular expressions
    phone = self.cleaned_data['phone']
    phone = re.sub('\D', '', phone)
    if 9 <= len(phone) <= 14:
      return phone
    elif len(phone) == 0:
      return None
    else:
      raise forms.ValidationError("number of digits incorrect")

class AssetCategoryForm(forms.Form):
  # choices must be formatted like [('group_title',(('1','opt1'),('2','opt2'))),]
  CATEGORY_ITEMS = []
  parent_categories = [c for c in Category.objects.all() if c.is_parent_category]
  for parent in parent_categories:
    sub_cats = ((str(parent.id),'other %s' % parent.name),)
    for sub in parent.sub_categories.all():
      keyword_string = " (%s)" % sub.keywords if sub.keywords else ""
      sub_cats = ((str(sub.id), "%s%s" % (sub.name,keyword_string)),) + sub_cats

    parent_keyword_string = " (%s)" % parent.keywords if parent.keywords else ""
    group = ("%s%s" % (parent.name, parent_keyword_string), sub_cats)
    CATEGORY_ITEMS.append(group)

  CATEGORY_ITEMS = [('','Category: None')] + CATEGORY_ITEMS

  category    = forms.ChoiceField(
                  widget=forms.Select(attrs={
                    'id':"-category",
                    'class':"asset-category autosave",
                  }),
                  choices = CATEGORY_ITEMS,
                  required = False)
