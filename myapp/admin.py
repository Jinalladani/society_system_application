from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from myapp.models import *


admin.site.register(User_Society_deatils)

admin.site.register(ExpenseCategory)

admin.site.register(IncomeCategory)

admin.site.register(BalanceValue)

admin.site.register(Members_Vendor_Account)

admin.site.register(MembersDeatilsValue)

admin.site.register(Income_Expense_LedgerValue1)

admin.site.register(FileStoreValue1)