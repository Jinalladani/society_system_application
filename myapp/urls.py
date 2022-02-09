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
    path('societyProfile', check_user(views.societyProfile), name="societyProfile"),
    path('registrationpage', views.registrationpage, name="registrationpage"),
    path('register', views.register, name="register"),
    path('forgot_password', views.forgot_password,name="forgot_password"),
    path('send_otp', views.send_otp, name="send-otp"),
    path('reset_password', views.reset_password, name="reset-password"),
    path('', check_user(views.index), name="index"),

    path('ExpensiveCategory', check_user(views.ExpensiveCategory), name="ExpensiveCategory"),
    path('editExpensiveCategory/<int:id>', check_user(views.editExpensiveCategory), name='editExpensiveCategory'),
    path('deleteExpensiveCategory/<int:id>', check_user(views.destroyExpensiveCategory), name="deleteExpensiveCategory"),
    path('addnewExpensiveCategory', check_user(views.addnewExpensiveCategory), name="addnewExpensiveCategory"),
    path('multi_deleteExpenseCategory', check_user(views.multi_deleteExpenseCategory), name="multi_deleteExpenseCategory"),
    path('all_deleteExpenseCategory',check_user(views.all_deleteExpenseCategory),name="all_deleteExpenseCategory"),

    path('IncomeCategoryshow', check_user(views.IncomeCategoryshow), name="IncomeCategoryshow"),
    path('editIncomeCategory/<int:id>', check_user(views.editIncomeCategory),name="editIncomeCategory"),
    path('deleteIncomeCategory/<int:id>', check_user(views.destroyIncomeCategory),name="deleteIncomeCategory"),
    path('multi_deleteIncomeCategory', check_user(views.multi_deleteIncomeCategory),name="multi_deleteIncomeCategory"),
    path('addnewIncomeCategory', check_user(views.addnewIncomeCategory),name="addnewIncomeCategory"),
    path('all_deleteIncomeCategory',check_user(views.all_deleteIncomeCategory),name="all_deleteIncomeCategory"),

    path('addincome_expense_ledger', check_user(views.addincome_expense_ledger),name="addincome_expense_ledger"),

    path('showBalance', check_user(views.showBalance), name="showBalance"),
    path('addnewBalance', check_user(views.addnewBalance),name="addnewBalance"),
    path('editBalance/<int:id>', check_user(views.editBalance),name="editBalance"),
    path('deleteBalance/<int:id>', views.destroyBalance,name="deleteBalance"),

    path('showMembers_vendor', check_user(views.showMembers_vendor), name="showMembers_vendor"),
    path('editMembers_vendor/<int:id>', check_user(views.editMembers_vendor),name="editMembers_vendor"),
    path('deleteMembers_vendor/<int:id>', views.destroyMembers_vendor,name="deleteMembers_vendor"),
    path('addnewMembers_vendor', check_user(views.addnewMembers_vendor),name="addnewMembers_vendor"),
    path('multi_deleteMembers_vendor', views.multi_deleteMembers_vendor,name="multi_deleteMembers_vendor"),
    path('all_deleteMembers_vendor',views.all_deleteMembers_vendor,name="all_deleteMembers_vendor"),

    path('export_users_xls', check_user(views.export_users_xls),name="export_users_xls"),
    path('export_users_xlsImcome', check_user(views.export_users_xlsImcome),name="export_users_xlsImcome"),
    path('export_users_xlsImembers', check_user(views.export_users_xlsImembers),name="export_users_xlsImembers"),

    path('upload_file', check_user(views.upload_file),name="upload_file"),
    path('simple_upload', check_user(views.simple_upload),name="simple_upload"),
    path('simple_uploadIncome', check_user(views.simple_uploadIncome),name="simple_uploadIncome"),
    path('simple_uploadMembers_Vendors', check_user(views.simple_uploadMembers_Vendors),name="simple_uploadMembers_Vendors"),

    path('income_expense_ledgerValue', check_user(views.income_expense_ledgerValue),name="income_expense_ledgerValue"),
    path('showincome_expense_ledger', check_user(views.showincome_expense_ledger), name="showincome_expense_ledger"),
    path('editIncome_expense_ledger/<int:id>', check_user(views.editIncome_expense_ledger),name="editIncome_expense_ledger"),
    path('deleteIncome_expense_ledger/<int:id>', check_user(views.destroyIncome_expense_ledger),name="deleteIncome_expense_ledger"),
    path('export_users_xlsLedger', check_user(views.export_users_xlsLedger),name="export_users_xlsLedger"),
    path('multi_deleteIncome_Expense_Ledger', check_user(views.multi_deleteIncome_Expense_Ledger),name="multi_deleteIncome_Expense_Ledger"),
    path('simple_uploadIncome_Expense_Ledger', check_user(views.simple_uploadIncome_Expense_Ledger),name="simple_uploadIncome_Expense_Ledger"),
    path('all_deleteIncome_Expense_Ledger',check_user(views.all_deleteIncome_Expense_Ledger),name="all_deleteIncome_Expense_Ledger"),

    path('demo/<int:id>', check_user(views.demo), name='demo'),

    path('cashWithdrawal', check_user(views.cashWithdrawal),name="cashWithdrawal"),
    path('cashWithdrawEntryValue', check_user(views.cashWithdrawEntryValue),name="cashWithdrawEntryValue"),
    path('cashDeposit', check_user(views.cashDeposit),name="cashDeposit"),
    path('cashDepositEntryValue', check_user(views.cashDepositEntryValue),name="cashDepositEntryValue"),

    path('sample_Excel', check_user(views.sample_Excel),name="sample_Excel"),
    path('download_excel_data', check_user(views.download_excel_data),name="download_excel_data"),
    path('export_csv', check_user(views.export_csv),name="export_csv"),
    path('destroyFile/<int:id>', check_user(views.destroyFile), name='deletefile'),

    path('showMembersDetails', check_user(views.showMembersDetails), name='showMembersDetails'),
    path('addnewMembersDetails', check_user(views.addnewMembersDetails),name="addnewMembersDetails"),
    path('editMembersDetails/<int:id>', check_user(views.editMembersDetails),name="editMembersDetails"),
    path('deletedMembersDetails/<int:id>', check_user(views.destroyMembersDetails),name="deletedMembersDetails"),
    path('multi_deleteMembersDetails', check_user(views.multi_deleteMembersDetails),name="multi_deleteMembersDetails"),
    path('all_deleteMembers',check_user(views.all_deleteMembers),name="all_deleteMembers"),
    path('export_users_xlsImembersDetails', check_user(views.export_users_xlsImembersDetails),name="export_users_xlsImembersDetails"),
    path('simple_uploadMembersDetails', check_user(views.simple_uploadMembersDetails),name="simple_uploadMembersDetails"),

    path('showSubUser', check_user(views.showSubUser), name="showSubUser"),
    path('addnewSubUser', check_user(views.addnewSubUser), name="addnewSubUser"),
    path('editSubUser/<int:id>', check_user(views.editSubUser),name="editSubUser"),
    path('deleteSubUser/<int:id>', check_user(views.deleteSubUser),name="deleteSubUser"),
    path('multi_deleteSubUser', check_user(views.multi_deleteSubUser),name="multi_deleteSubUser"),
    path('all_deleteSubUser',check_user(views.all_deleteSubUser),name="all_deleteSubUser"),

    path('AssetCategory', check_user(views.AssetCategory), name="AssetCategory"),
    path('addnewAssetCategory', check_user(views.addnewAssetCategory),name="addnewAssetCategory"),
    path('editAssetCategory/<int:id>', check_user(views.editAssetCategory),name="editAssetCategory"),
    path('deleteAssetCategory/<int:id>', check_user(views.deleteAssetCategory), name="deleteAssetCategory"),
    path('multi_deleteAssetCategory', check_user(views.multi_deleteAssetCategory),name="multi_deleteAssetCategory"),
    path('all_deleteAssetCategory',check_user(views.all_deleteAssetCategory),name="all_deleteAssetCategory"),
    path('export_users_xlsIassetCategory',check_user(views.export_users_xlsIassetCategory),name="export_users_xlsIassetCategory"),
    path('simple_uploadAssentCategory',check_user(views.simple_uploadAssentCategory),name="simple_uploadAssentCategory"),

    path('Asset_InventoryCategory', check_user(views.Asset_InventoryCategory), name="Asset_InventoryCategory"),
    path('addnewAsset_InventoryCategory', check_user(views.addnewAsset_InventoryCategory),name="addnewAsset_InventoryCategory"),
    path('addNewRecordAssent_Inventory', check_user(views.addNewRecordAssent_Inventory),name="addNewRecordAssent_Inventory"),
    path('editAsset_InventoryCategory/<int:id>', check_user(views.editAsset_InventoryCategory),name="editAsset_InventoryCategory"),
    path('destroyAsset_InventoryCategory/<int:id>', check_user(views.destroyAsset_InventoryCategory),
         name="deleteAsset_InventoryCategory"),
    path('multi_deleteAsset_InventoryCategory', check_user(views.multi_deleteAsset_InventoryCategory),name="multi_deleteAsset_InventoryCategory"),
    path('all_deleteAsset_InventoryCategory',check_user(views.all_deleteAsset_InventoryCategory),name="all_deleteAsset_InventoryCategory"),
    path('export_users_xlsIassetInventory',check_user(views.export_users_xlsIassetInventory),name="export_users_xlsIassetInventory"),
    path('simple_uploadAssentInventoryCategory',check_user(views.simple_uploadAssentInventoryCategory),name="simple_uploadAssentInventoryCategory"),

    path('sdetail/<int:id>', check_user(views.download_zipfile), name='dzip'),

    path('send_sms',check_user(views.send_sms),name="send_sms"),
    path('get_message',check_user(views.get_message),name='get_message'),

    path('showincome_with_id/<str>', views.showincome_with_id, name='showincome_with_id'),
    path('showmembers_with_id/<str>',views.showmembers_with_id,name='showmembers_with_id'),
    path('showmembers_with_bank/<str>/<cheader>', views.showmembers_with_bank,name='showmembers_with_bank'),


]
