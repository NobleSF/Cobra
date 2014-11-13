from django import template
register = template.Library()

@register.inclusion_tag('checkout/manual_checkout.html')
def manual_checkout_tag(cart):
  from apps.public.controller.forms import CartForm
  form = CartForm()
  try:
    form.fields['notes'].initial        = cart.getData('notes')
    form.fields['receipt'].initial      = cart.getData('receipt')
  except: pass

  return {'form': form}
