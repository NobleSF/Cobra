from django import forms
from apps.public.models import Cart

class CartForm(forms.ModelForm):
  class Meta:
    model = Cart
    fields = ('email', 'name', 'address1', 'address2', 'city', 'state', 'postal_code', 'country')
