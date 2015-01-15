from django import template
from django.utils import timezone

register = template.Library()

@register.inclusion_tag('commissions/commission_list_item.html')
def commission_list_item(commission):
  return {'commission': commission}

@register.inclusion_tag('commissions/commission_details.html')
def commission_details(commission):
  details = [ # ['title', value, True #editable],
    [
      'requested length',
      commission.length,
      True,
    ],
    [
      'actual length',
      commission.product.length if commission.product else None,
      False,
    ],
    [
      'requested width',
      commission.width,
      True,
    ],
    [
      'actual width',
      commission.product.width if commission.product else None,
      False,
    ],
    [
      'quantity',
      commission.quantity,
      True,
    ],
    [
      'price',
      commission.product.price if commission.product else None,
      False,
    ],
    [
      'days to complete',
      "%d days" % commission.days_to_complete if commission.days_to_complete else "",
      True,
    ],
    [
      'progress',
      "%d%%" % commission.progress,
      True,
    ],
    [
      'weight',
      commission.product.weight if commission.product else commission.estimated_weight,
      True,
    ],
    [
      'expected completion date',
      (commission.estimated_completion_date.strftime("%d/%m/%y")
        if commission.estimated_completion_date else None),
      False,
    ],
    [
      'country',
      commission.customer.country if commission.customer else None,
      False,
    ],
    [
      'shipping cost',
      commission.product.shipping_cost if commission.product else None,
      False,
    ],
    [
      'anou fee',
      commission.product.anou_fee if commission.product else None,
      False,
    ],
    [
      'stripe fee',
      commission.product.stripe_fee if commission.product else None,
      False,
    ],
    [
      'conversion',
      commission.product.exchange_rate if commission.product else None,
      False,
    ],
    [
      'invoiced price',
      commission.estimated_display_price,
      False,
    ],
    [
      'payment receipt',
      commission.payment_receipt,
      False,
    ]
  ]

  return {'commission': commission, 'details':details}