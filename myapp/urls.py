"""userinterface URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from .check_me import check_user, login_user

urlpatterns = [
    path('login', login_user(views.login), name="login"),
    path('logout', views.logout, name="logout"),
    path('societyProfile', views.societyProfile, name="societyProfile"),
    path('registrationpage', views.registrationpage, name="registrationpage"),
    path('register', views.register, name="register"),
    path('forgot_password', views.forgot_password),
    path('send_otp', views.send_otp, name="send-otp"),
    path('reset_password', views.reset_password, name="reset-password"),
    path('', check_user( views.index), name="index"),

    path('ExpensiveCategory', views.ExpensiveCategory, name="ExpensiveCategory"),
    path('editExpensiveCategory/<int:id>', views.editExpensiveCategory, name='editExpensiveCategory'),
    path('deleteExpensiveCategory/<int:id>', views.destroyExpensiveCategory, name="deleteExpensiveCategory"),
    path('addnewExpensiveCategory', views.addnewExpensiveCategory, name="addnewExpensiveCategory"),
    path('multi_deleteExpenseCategory', views.multi_deleteExpenseCategory, name="multi_deleteExpenseCategory"),
    path('all_deleteExpenseCategory',views.all_deleteExpenseCategory,name="all_deleteExpenseCategory"),

    path('IncomeCategoryshow', views.IncomeCategoryshow, name="IncomeCategoryshow"),
    path('editIncomeCategory/<int:id>', views.editIncomeCategory,name="editIncomeCategory"),
    path('deleteIncomeCategory/<int:id>', views.destroyIncomeCategory,name="deleteIncomeCategory"),
    path('multi_deleteIncomeCategory', views.multi_deleteIncomeCategory,name="multi_deleteIncomeCategory"),
    path('addnewIncomeCategory', views.addnewIncomeCategory,name="addnewIncomeCategory"),
    path('all_deleteIncomeCategory',views.all_deleteIncomeCategory,name="all_deleteIncomeCategory"),

    path('addincome_expense_ledger', views.addincome_expense_ledger,name="addincome_expense_ledger"),

    path('showBalance', views.showBalance, name="showBalance"),
    path('addnewBalance', views.addnewBalance,name="addnewBalance"),
    path('editBalance/<int:id>', views.editBalance,name="editBalance"),
    path('deleteBalance/<int:id>', views.destroyBalance,name="deleteBalance"),

    path('showMembers_vendor', views.showMembers_vendor, name="showMembers_vendor"),
    path('editMembers_vendor/<int:id>', views.editMembers_vendor,name="editMembers_vendor"),
    path('deleteMembers_vendor/<int:id>', views.destroyMembers_vendor,name="deleteMembers_vendor"),
    path('addnewMembers_vendor', views.addnewMembers_vendor),
    path('multi_deleteMembers_vendor', views.multi_deleteMembers_vendor),
    path('all_deleteMembers_vendor',views.all_deleteMembers_vendor,name="all_deleteMembers_vendor"),

    path('export_users_xls', views.export_users_xls),
    path('export_users_xlsImcome', views.export_users_xlsImcome),
    path('export_users_xlsImembers', views.export_users_xlsImembers),

    path('upload_file', views.upload_file),
    path('simple_upload', views.simple_upload),
    path('simple_uploadIncome', views.simple_uploadIncome),
    path('simple_uploadMembers_Vendors', views.simple_uploadMembers_Vendors),

    path('income_expense_ledgerValue', views.income_expense_ledgerValue),
    path('showincome_expense_ledger', views.showincome_expense_ledger, name="showincome_expense_ledger"),
    path('editIncome_expense_ledger/<int:id>', views.editIncome_expense_ledger),
    path('deleteIncome_expense_ledger/<int:id>', views.destroyIncome_expense_ledger),
    path('export_users_xlsLedger', views.export_users_xlsLedger),
    path('multi_deleteIncome_Expense_Ledger', views.multi_deleteIncome_Expense_Ledger),
    path('simple_uploadIncome_Expense_Ledger', views.simple_uploadIncome_Expense_Ledger),
    path('all_deleteIncome_Expense_Ledger',views.all_deleteIncome_Expense_Ledger,name="all_deleteIncome_Expense_Ledger"),

    path('demo/<int:id>', views.demo, name='demo'),

    path('cashWithdrawal', views.cashWithdrawal),
    path('cashWithdrawEntryValue', views.cashWithdrawEntryValue),
    path('cashDeposit', views.cashDeposit),
    path('cashDepositEntryValue', views.cashDepositEntryValue),

    path('sample_Excel', views.sample_Excel),
    path('download_excel_data', views.download_excel_data),
    path('export_csv', views.export_csv),
    path('destroyFile/<int:id>', views.destroyFile, name='deletefile'),

    path('showMembersDetails', views.showMembersDetails, name='showMembersDetails'),
    path('addnewMembersDetails', views.addnewMembersDetails),
    path('editMembersDetails/<int:id>', views.editMembersDetails),
    path('deletedMembersDetails/<int:id>', views.destroyMembersDetails),
    path('multi_deleteMembersDetails', views.multi_deleteMembersDetails),
    path('all_deleteMembers',views.all_deleteMembers,name="all_deleteMembers"),
    path('export_users_xlsImembersDetails', views.export_users_xlsImembersDetails),
    path('simple_uploadMembersDetails', views.simple_uploadMembersDetails),

    path('showSubUser', views.showSubUser, name="showSubUser"),
    path('addnewSubUser', views.addnewSubUser, name="subuser"),
    path('editSubUser/<int:id>', views.editSubUser),
    path('deleteSubUser/<int:id>', views.deleteSubUser),
    path('multi_deleteSubUser', views.multi_deleteSubUser),
    path('all_deleteSubUser',views.all_deleteSubUser,name="all_deleteSubUser"),

    path('AssetCategory', views.AssetCategory, name="AssetCategory"),
    path('addnewAssetCategory', views.addnewAssetCategory),
    path('editAssetCategory/<int:id>', views.editAssetCategory),
    path('deleteAssetCategory/<int:id>', views.deleteAssetCategory, name="deleteAssetCategory"),
    path('multi_deleteAssetCategory', views.multi_deleteAssetCategory),
    path('all_deleteAssetCategory',views.all_deleteAssetCategory,name="all_deleteAssetCategory"),
    path('export_users_xlsIassetCategory',views.export_users_xlsIassetCategory),
    path('simple_uploadAssentCategory',views.simple_uploadAssentCategory),

    path('Asset_InventoryCategory', views.Asset_InventoryCategory, name="Asset_InventoryCategory"),
    path('addnewAsset_InventoryCategory', views.addnewAsset_InventoryCategory),
    path('addNewRecordAssent_Inventory', views.addNewRecordAssent_Inventory),
    path('editAsset_InventoryCategory/<int:id>', views.editAsset_InventoryCategory),
    path('destroyAsset_InventoryCategory/<int:id>', views.destroyAsset_InventoryCategory,
         name="deleteAsset_InventoryCategory"),
    path('multi_deleteAsset_InventoryCategory', views.multi_deleteAsset_InventoryCategory),
    path('all_deleteAsset_InventoryCategory',views.all_deleteAsset_InventoryCategory,name="all_deleteAsset_InventoryCategory"),
    path('export_users_xlsIassetInventory',views.export_users_xlsIassetInventory),
    path('simple_uploadAssentInventoryCategory',views.simple_uploadAssentInventoryCategory),

]
