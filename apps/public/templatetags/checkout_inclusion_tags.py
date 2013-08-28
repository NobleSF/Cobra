from django import template
register = template.Library()

@register.inclusion_tag('checkout/manual_checkout.html')
def manual_checkout_tag(cart):
  from apps.public.controller.forms import ManualCheckoutForm

  form = ManualCheckoutForm()

  try:
    form.fields['address1'].initial     = cart.getData('address1')
    form.fields['address2'].initial     = cart.getData('address2')
    form.fields['city'].initial         = cart.getData('city')
    form.fields['state'].initial        = cart.getData('state')
    form.fields['postal_code'].initial  = cart.getData('postal_code')
    form.fields['country'].initial      = cart.getData('country')
    form.fields['notes'].initial        = cart.getData('notes')
    form.fields['receipt'].initial      = cart.getData('receipt')
  except: pass

  return {'form': form}
