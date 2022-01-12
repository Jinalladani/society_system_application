from django.db import models
from django.contrib.auth.models import AbstractUser, User
from accounts.models import User


# class Society(models.Model):
#     user_key = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
#     email = models.EmailField(unique=True)
#     phone_no = models.CharField(max_length=10, blank=True, null=True)
#     contact_name = models.CharField(max_length=500)
#     society_name = models.CharField(max_length=500)
#     society_address = models.CharField(max_length=500)
#     city = models.CharField(max_length=200)
#     pin_code = models.CharField(max_length=10)
#     state = models.CharField(max_length=100, default='Gujarat')
#     country = models.CharField(max_length=100)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True, blank=False)
#     updated_at = models.DateTimeField(auto_now=True, blank=False)
#
#     def __str__(self):
#         return self.name


class SocietyDeatils(models.Model):
    user_key = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=10, blank=True, null=True)
    contact_name = models.CharField(max_length=500)
    society_name = models.CharField(max_length=500)
    society_address = models.CharField(max_length=500)
    city = models.CharField(max_length=200)
    pin_code = models.CharField(max_length=10)
    state = models.CharField(max_length=100, default='Gujarat')
    country = models.CharField(max_length=100)
    society_registration_number = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)


class Society(models.Model):
    user_key = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_no = models.CharField(max_length=10, blank=True, null=True)
    contact_name = models.CharField(max_length=500)
    society_name = models.CharField(max_length=500)
    society_address = models.CharField(max_length=500)
    city = models.CharField(max_length=200)
    pin_code = models.CharField(max_length=10)
    state = models.CharField(max_length=100, default='Gujarat')
    country = models.CharField(max_length=100)
    society_registration_number = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)


class ExpenseCategory(models.Model):
    society_key = models.ForeignKey(Society, on_delete=models.SET_NULL, null=True)
    category_name = models.CharField(max_length=200)


class AssentCategory1(models.Model):
    society_key = models.ForeignKey(Society, on_delete=models.SET_NULL, null=True)
    category_name = models.CharField(max_length=200)


class Asset_InventoryCategoryValue1(models.Model):
    society_key = models.ForeignKey(Society, on_delete=models.SET_NULL, null=True)
    itemName = models.CharField(max_length=200, null=True, blank=True)
    assetCategory = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.FloatField(max_length=200, null=True, blank=True)
    purchasePrice = models.FloatField(max_length=200, null=True, blank=True)
    deprecatedPrice = models.FloatField(max_length=200, null=True, blank=True)
    onDate = models.DateField(null=True, blank=True)
    totalCost = models.FloatField(max_length=200, null=True, blank=True)
    marketValue = models.FloatField(max_length=200, null=True, blank=True)


class IncomeCategory(models.Model):
    society_key = models.ForeignKey(Society, on_delete=models.SET_NULL, null=True)
    category_name = models.CharField(max_length=200)


class BalanceValue(models.Model):
    society_key = models.ForeignKey(Society, on_delete=models.SET_NULL, null=True)
    account = models.CharField(max_length=100)
    balance_amount = models.FloatField(max_length=500)


class Members_Vendor_Account(models.Model):
    society_key = models.ForeignKey(Society, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)


class UserPermission(models.Model):
    user_key = models.OneToOneField(User, on_delete=models.CASCADE, null = True, blank = True)
    society_key = models.ForeignKey(Society, blank=True, null=True, on_delete=models.CASCADE)
    is_society_admin = models.BooleanField(default=False)
    role = models.CharField(max_length=250)
    is_active = models.BooleanField(default=False)
    is_edit = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)

    def _str_(self):
        return str(self.user_key)


class MembersDeatilsValue(models.Model):
    society_key = models.ForeignKey(Society, on_delete=models.SET_NULL, null=True)
    flatNo = models.CharField(max_length=200)
    primaryName = models.CharField(max_length=200, null=True, blank=True)
    primaryContactNo = models.CharField(max_length=10, null=True, blank=True)
    secondaryName = models.CharField(max_length=200, null=True, blank=True)
    secondaryContactNo = models.CharField(max_length=10, null=True, blank=True)
    accountingName = models.CharField(max_length=200, null=True, blank=True)
    whatsappContactNo = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    residence = models.CharField(max_length=100)

    def _str_(self):
        return str(self.society_key)

class Income_Expense_LedgerValue1(models.Model):
    society_key = models.ForeignKey(Society, on_delete=models.SET_NULL, null=True)
    dateOn = models.DateField()
    type = models.CharField(max_length=100)
    amount = models.FloatField(max_length=100)
    category_header = models.CharField(max_length=100, null=True, blank=True)
    from_or_to_account = models.CharField(max_length=100, null=True, blank=True)
    transaction_type = models.CharField(max_length=100)
    transaction_details = models.CharField(max_length=100, null=True, blank=True)
    voucherNo_or_invoiceNo = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='images/', verbose_name='image', null=True, blank=True)
    remark = models.TextField(max_length=500, null=True, blank=True)
    opening_balance_cash = models.FloatField(max_length=100, blank=True, null=True)
    closing_balance_cash = models.FloatField(max_length=100, blank=True, null=True)
    opening_balance_bank = models.FloatField(max_length=100, blank=True, null=True)
    closing_balance_bank = models.FloatField(max_length=100, blank=True, null=True)
    entry_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return  str(self.society_key)


class FileStoreValue1(models.Model):
    society_key = models.ForeignKey(Society, on_delete=models.SET_NULL, null=True)
    income_Expense_LedgerId = models.ForeignKey(Income_Expense_LedgerValue1, on_delete=models.CASCADE)
    text = models.CharField(max_length=100, null=True, blank=True)
    type_file = models.FileField(upload_to='filestore/', verbose_name='file', null=True, blank=True)
