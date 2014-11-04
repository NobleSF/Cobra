from django.test import TestCase
from apps.communication.models.sms import SMS as SMSModel
from apps.communication.controller import sms

class SMSTestCase(TestCase):
  def test_create(self):
    """
    Tests that an SMS can be created and saved
    """
    sms_instance = SMSModel.objects.create()
    sms_instance.from_number = "1234567890"
    sms_instance.to_number = "0987654321"
    sms_instance.message = "Labas?"
    sms_instance.auto_reply = "Labas, Hamdullah"
    sms_instance.telerivet_id = "some_id_number_12345"
    sms_instance.save()

    self.assertIsInstance(sms_instance, SMSModel)
    self.assertIsNone(sms_instance.status)

  def test_send(self):
    """
    Tests that an SMS sent with Telerivet
    """
    sms_instance = sms.sendSMS("running a test", "5558675309")

    #sms_instance exists in db
    self.assertIsInstance(sms_instance, SMSModel, "SMS not created")
    self.assertEqual(sms_instance, SMSModel.objects.get(id=sms_instance.id), "SMS not saved")

    #sms contains the right content
    self.assertEquals(sms_instance.message, "running a test", "SMS message bad")
    self.assertEquals(sms_instance.to_number, "5558675309", "SMS recipient bad")
    self.assertIsNotNone(sms_instance.from_number, "SMS sender bad")
    self.assertIsNotNone(sms_instance.telerivet_id, "SMS Telerivet ID not found")

  def test_understanding(self):
    """
    Tests that SMS messages can be properly understood
    """
    from apps.admin.models.account import Account
    account = Account(password="gobbly gook")
    account.save()
    from apps.seller.models.seller import Seller
    seller = Seller(account=account)
    seller.save()
    from apps.seller.models.product import Product
    product = Product(seller=seller)
    product.save()

    tracking_test_cases = ["CP123456789012MA", "RR123456MA"]#, "CP 12345678 MA"
    for tracking_num in tracking_test_cases:
      message_tests = [
        "%d %s" % (product.id, tracking_num),
        "  %d    %s   " % (product.id, tracking_num),
        "%d something %s random" % (product.id, tracking_num),
        #"%s %d" % (tracking_num, product.id),
      ]
      for message in message_tests:
        result = sms.understandMessage(message)
        self.assertIsNot(result, False, "SMS message \"%s\" not understood" % message)
        (found_product_id, actions) = result
        self.assertEqual(product.id, int(found_product_id), "SMS product id not identified")
        self.assertEqual(actions['tracking_number'], tracking_num, "SMS tracking \"%s\" not found in \"%s\"" % (tracking_num, message))
