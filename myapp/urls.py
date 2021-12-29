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
from .check_me import check_user

urlpatterns = [
                  path('', views.loginpage, name="loginpage"),
                  path('login', views.login,name="login"),
                  path('logout', views.logout,name="logout"),
                  path('societyProfile',views.societyProfile,name="societyProfile"),
                  path('registrationpage', views.registrationpage,name="registrationpage"),
                  path('register', views.register,name="register"),
                  path('forgot_password',views.forgot_password),
                  path('send_otp',views.send_otp,name="send-otp"),
                  path('reset_password',views.reset_password,name="reset-password"),
                  path('index', views.index, name="index"),
                  path('ExpensiveCategory', views.ExpensiveCategory, name="ExpensiveCategory"),
                  path('editExpensiveCategory/<int:id>', views.editExpensiveCategory, name='editExpensiveCategory'),
                  path('deleteExpensiveCategory/<int:id>', views.destroyExpensiveCategory,name="deleteExpensiveCategory"),
                  path('addnewExpensiveCategory', views.addnewExpensiveCategory,name="addnewExpensiveCategory"),
                  path('multi_deleteExpenseCategory', views.multi_deleteExpenseCategory,name="multi_deleteExpenseCategory"),
                  path('IncomeCategoryshow', views.IncomeCategoryshow, name="IncomeCategoryshow"),
                  path('editIncomeCategory/<int:id>', views.editIncomeCategory),
                  # path('updateIncomeCategory/<int:id>', views.updateIncomeCategory),
                  path('deleteIncomeCategory/<int:id>', views.destroyIncomeCategory),
                  path('multi_deleteIncomeCategory', views.multi_deleteIncomeCategory),
                  # path('AssentCategory',views.AssentCategory),
                  path('addnewIncomeCategory', views.addnewIncomeCategory),
                  path('addincome_expense_ledger', views.addincome_expense_ledger),
                  path('showBalance', views.showBalance, name="showBalance"),
                  path('addnewBalance', views.addnewBalance),
                  path('editBalance/<int:id>', views.editBalance),
                  # path('updateBalance/<int:id>', views.updateBalance),
                  path('deleteBalance/<int:id>', views.destroyBalance),
                  path('showMembers_vendor', views.showMembers_vendor, name="showMembers_vendor"),
                  path('editMembers_vendor/<int:id>', views.editMembers_vendor),
                  # path('updateMembers_vendor/<int:id>', views.updateMembers_vendor),
                  path('deleteMembers_vendor/<int:id>', views.destroyMembers_vendor),
                  path('addnewMembers_vendor', views.addnewMembers_vendor),
                  path('multi_deleteMembers_vendor', views.multi_deleteMembers_vendor),
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
                  # path('updateIncome_expense_ledger/<int:id>', views.updateIncome_expense_ledger),
                  path('deleteIncome_expense_ledger/<int:id>', views.destroyIncome_expense_ledger),
                  path('export_users_xlsLedger', views.export_users_xlsLedger),
                  path('multi_deleteIncome_Expense_Ledger', views.multi_deleteIncome_Expense_Ledger),
                  path('simple_uploadIncome_Expense_Ledger', views.simple_uploadIncome_Expense_Ledger),
                  path('demo/<int:id>', views.demo, name='demo'),
                  path('cashWithdrawal', views.cashWithdrawal),
                  path('cashWithdrawEntryValue', views.cashWithdrawEntryValue),
                  path('cashDeposit', views.cashDeposit),
                  path('cashDepositEntryValue', views.cashDepositEntryValue),
                  path('sample_Excel', views.sample_Excel),
                  path('download_excel_data', views.download_excel_data),
                  path('export_csv', views.export_csv),
                  # path('demo/file_store', views.file_store, name="file_store"),
                  path('destroyFile/<int:id>', views.destroyFile, name='deletefile'),
                  path('showMembersDetails', views.showMembersDetails, name='showMembersDetails'),
                  path('addnewMembersDetails', views.addnewMembersDetails),
                  path('editMembersDetails/<int:id>', views.editMembersDetails),
                  # path('updateMembersDetails/<int:id>', views.updateMembersDetails),
                  path('deletedMembersDetails/<int:id>', views.destroyMembersDetails),
                  path('multi_deleteMembersDetails',views.multi_deleteMembersDetails),
                  path('export_users_xlsImembersDetails', views.export_users_xlsImembersDetails),
                  path('simple_uploadMembersDetails', views.simple_uploadMembersDetails),
                  path('showSubUser',views.showSubUser,name="showSubUser"),
                  path('addnewSubUser',views.addnewSubUser,name="addnewSubUser"),
                  path('AssetCategory',views.AssetCategory,name="AssetCategory"),
                  path('addnewAssetCategory',views.addnewAssetCategory),
                  path('editAssetCategory/<int:id>', views.editAssetCategory),
                  path('deleteAssetCategory/<int:id>', views.deleteAssetCategory,name="deleteAssetCategory"),
                  path('multi_deleteAssetCategory', views.multi_deleteAssetCategory),

                  path('Asset_InventoryCategory',views.Asset_InventoryCategory,name="Asset_InventoryCategory"),
                  path('addnewAsset_InventoryCategory',views.addnewAsset_InventoryCategory),
                  path('addNewRecordAssent_Inventory',views.addNewRecordAssent_Inventory),
                  path('editAsset_InventoryCategory/<int:id>',views.editAsset_InventoryCategory),
                  path('destroyAsset_InventoryCategory/<int:id>',views.destroyAsset_InventoryCategory,name="deleteAsset_InventoryCategory"),
                  path('multi_deleteAsset_InventoryCategory',views.multi_deleteAsset_InventoryCategory),

              ]

