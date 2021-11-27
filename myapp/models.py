from django.db import models


class User_Society_deatils(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    contact_name = models.CharField(max_length=500)
    otp = models.IntegerField(default=459)
    moblie_no = models.CharField(unique=True, max_length=10)
    society_name = models.CharField(max_length=500)
    society_address = models.CharField(max_length=500)
    city = models.CharField(max_length=200)
    pin_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    society_registration_number = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_verfied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)


# class Employee(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     contact = models.CharField(max_length=15)
#     age = models.CharField(max_length=3)
#     status = models.BooleanField(default=False)
#
#     class Meta:
#         db_table = "employee"


class ExpenseCategory(models.Model):
    category_name = models.CharField(unique=True, max_length=200)


class IncomeCategory(models.Model):
    category_name = models.CharField(unique=True, max_length=200)


class BalanceValue(models.Model):
    account = models.CharField(unique=True, max_length=100)
    balance_amount = models.FloatField(max_length=500)


class Members_Vendor_Account(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)


class MembersDeatils(models.Model):
    flatNo = models.CharField(max_length=200)
    primaryName = models.CharField(max_length=200, null=True, blank=True)
    primaryContactNo = models.CharField(max_length=10, null=True, blank=True)
    secondaryName = models.CharField(max_length=200, null=True, blank=True)
    secondaryContactNo = models.CharField(max_length=10, null=True, blank=True)
    accountingName = models.CharField(max_length=200, null=True, blank=True)
    whatsappContactNo = models.CharField(max_length=10, null=True, blank=True)


class MembersDeatilsValue(models.Model):
    flatNo = models.CharField(max_length=200)
    primaryName = models.CharField(max_length=200, null=True, blank=True)
    primaryContactNo = models.CharField(max_length=10, null=True, blank=True)
    secondaryName = models.CharField(max_length=200, null=True, blank=True)
    secondaryContactNo = models.CharField(max_length=10, null=True, blank=True)
    accountingName = models.CharField(max_length=200, null=True, blank=True)
    whatsappContactNo = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(unique=True)
    residence = models.CharField(max_length=100)


class Income_Expense_LedgerValue1(models.Model):
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
    opening_balance_cash = models.FloatField(max_length=100)
    closing_balance_cash = models.FloatField(max_length=100)
    opening_balance_bank = models.FloatField(max_length=100)
    closing_balance_bank = models.FloatField(max_length=100)
    entry_time = models.DateTimeField(null=True, blank=True)


class FileStoreValue1(models.Model):
    income_Expense_LedgerId = models.ForeignKey(Income_Expense_LedgerValue1, on_delete=models.CASCADE)
    text = models.CharField(max_length=100, null=True, blank=True)
    type_file = models.FileField(upload_to='filestore/', verbose_name='file', null=True, blank=True)
