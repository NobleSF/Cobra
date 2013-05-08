"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):
  def test_basic_addition(self):
    """
    Tests that 1 + 1 always equals 2.
    """
    self.assertEqual(1 + 1, 2)

class SellerTests(TestCase):

  def test_CreateSeller(self):
    """
    Tests the creation of a seller account in the database
    """
    from controllers.admin import Account
    from controllers.seller import Seller

    account = Account()
    seller = Seller()

    new_account = account.new("username","password")
    seller_account = seller.new(new_account)

    self.assertIsInstance(seller_account, Seller)


if __name__ == "__main__":
  SimpleTest.test_basic_addition();
  SellerTests.test_CreateSeller();
