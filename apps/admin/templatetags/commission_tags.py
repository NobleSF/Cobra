from django import template
from django.utils import timezone

register = template.Library()

@register.inclusion_tag('commissions/commission_list_item.html')
def commission_list_item(commission):
  return {'commission': commission}

@register.inclusion_tag('commissions/commission_details.html')
def commission_details(commission):
  product_details = [ # ['title', value, True #editable],
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
      'expected completion date',
      (commission.estimated_completion_date.strftime("%d/%m/%y")
        if commission.estimated_completion_date else None),
      False,
    ],
    [
      'quantity',
      commission.quantity,
      True,
    ],
    [
      'requested length',
      commission.length,
      True,
    ],
    [
      'actual length',
      commission.product.length if commission.product and commission.product.is_active else None,
      False,
    ],
    [
      'requested width',
      commission.width,
      True,
    ],
    [
      'actual width',
      commission.product.width if commission.product and commission.product.is_active else None,
      False,
    ],
    [
      'estimated weight',
      commission.estimated_weight,
      False,
    ],
    [
      'actual weight',
      commission.product.weight if commission.product and commission.product.is_active else None,
      False,
    ],
    [
      'country',
      commission.customer.country if commission.customer else None,
      True,
    ],
  ]

  pricing_details = [ # ['title', value, True #editable],
    [
      'estimated price Dh',
      commission.estimated_artisan_price,
      False,
    ],
    [
      'actual price Dh',
      commission.product.price if commission.product else None,
      False,
    ],
    [
      'shipping cost Dh',
      commission.product.shipping_cost if commission.product else None,
      False,
    ],
    [
      'anou fee',
      "%.0f" % commission.product.anou_fee if commission.product else None,
      False,
    ],
    [
      'conversion',
      "%.2f" % commission.product.exchange_rate if commission.product else None,
      False,
    ],
    [
      'stripe fee',
      "%.0f" % commission.product.stripe_fee if commission.product else None,
      False,
    ],
    [
      'invoice price $',
      commission.estimated_display_price,
      False if commission.invoice_paid else True,
    ],
  ]
  if commission.invoice_paid:
    pricing_details.append([
      'payment receipt',
      commission.payment_receipt,
      False,
    ])

  return {'commission':       commission,
          'product_details':  product_details,
          'pricing_details':  pricing_details,
         }
