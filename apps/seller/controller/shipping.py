from math import ceil as roundUp

def calculateShippingCost(weight, shipping_option):
  shipping_cost = 9999
  rates = {}

  if (shipping_option.country.code == 'MA' and
      int(weight) <= 450 and
      shipping_option.name == 'Envelope'):
    rates = {
      '20': '14',
      '40': '29.5',
      '60': '35.7',
      '80': '42',
      '100': '48.2',
      '150': '80.9',
      '200': '93.3',
      '250': '112',
      '300': '150',
      '350': '168.7',
      '400': '181.1',
      '450': '199.8',
    }

  elif (shipping_option.country.code == 'MA'): #Package shipping_option
    rates = {
      '1000': '202',
      '2000': '290',
      '3000': '376',
      '4000': '463',
      '5000': '550',
      '6000': '638',
      '7000': '726',
      '8000': '815',
      '9000': '904',
      '10000': '993',
      '11000': '1082',
      '12000': '1171',
      '13000': '1261'
    }

  for weight_limit, cost in rates.iteritems():
    if int(weight) <= int(weight_limit) and float(cost) < shipping_cost:
      shipping_cost = float(cost)

  return int(roundUp(shipping_cost))
