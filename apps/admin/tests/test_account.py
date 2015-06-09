from django.test import TestCase
from apps.admin.models.account import OldAccount
from apps.admin.views.account import processPassword

class AccountTest(TestCase):
  def setUp(self):
    self.username = "Coop-Milk-Sport"
    self.email = "test+coop-milk-sport@theanou.com"
    self.phone = "21212345678"
    self.password = "1234abcdEFGH!@#$"

    OldAccount.objects.create(
      username=self.username,
      email=self.email,
      phone=self.phone,
      password=processPassword(self.password)
    )

  def test_password_encryption(self):
    """
      Tests the ability to encrypt passwords
    """
    account = OldAccount.objects.get(username=self.username)
    #encrypted password generated
    self.assertIsNotNone(account.password)
    self.assertEqual(processPassword(self.password), account.password)
    #encrypetd password is not same as original
    self.assertNotEqual(self.password, account.password)

  def test_create_account(self):
    """
    Tests the creation of an account in the DB model
    """
    account = OldAccount.objects.get(username=self.username)
    self.assertIsNotNone(account)
    self.assertEqual(account.username, self.username)
    self.assertEqual(account.email, self.email)
    self.assertEqual(account.phone, self.phone)

  def test_login(self):
    """
    Tests the login options for users
    """
    pass