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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index', views.index, name="index"),
    path('', views.loginpage, name="loginpage"),
    path('login', views.login),
    path('logout', views.logout),
    # path('multi_delete', views.multi_delete),
    path('registrationpage', views.registrationpage),
    path('register', views.register),
    path('ExpensiveCategory', views.ExpensiveCategory, name="ExpensiveCategory"),
    path('editExpensiveCategory/<int:id>', views.editExpensiveCategory),
    path('updateExpensiveCategory/<int:id>', views.updateExpensiveCategory),
    path('deleteExpensiveCategory/<int:id>', views.destroyExpensiveCategory),
    path('addnewExpensiveCategory', views.addnewExpensiveCategory),
    path('multi_deleteExpenseCategory', views.multi_deleteExpenseCategory),
    path('IncomeCategoryshow', views.IncomeCategoryshow, name="IncomeCategoryshow"),
    path('editIncomeCategory/<int:id>', views.editIncomeCategory),
    path('updateIncomeCategory/<int:id>', views.updateIncomeCategory),
    path('deleteIncomeCategory/<int:id>', views.destroyIncomeCategory),
    path('multi_deleteIncomeCategory', views.multi_deleteIncomeCategory),
    path('addnewIncomeCategory', views.addnewIncomeCategory),
    path('addincome_expense_ledger', views.addincome_expense_ledger),
    path('showBalance', views.showBalance, name="showBalance"),
    path('addnewBalance', views.addnewBalance),
    path('editBalance/<int:id>', views.editBalance),
    path('updateBalance/<int:id>', views.updateBalance),
    path('deleteBalance/<int:id>', views.destroyBalance),
    path('showMembers_vendor', views.showMembers_vendor, name="showMembers_vendor"),
    path('editMembers_vendor/<int:id>', views.editMembers_vendor),
    path('updateMembers_vendor/<int:id>', views.updateMembers_vendor),
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
    path('updateIncome_expense_ledger/<int:id>', views.updateIncome_expense_ledger),
    path('deleteIncome_expense_ledger/<int:id>', views.destroyIncome_expense_ledger),
    path('export_users_xlsLedger', views.export_users_xlsLedger),
    path('multi_deleteIncome_Expense_Ledger', views.multi_deleteIncome_Expense_Ledger),
    path('simple_uploadIncome_Expense_Ledger', views.simple_uploadIncome_Expense_Ledger),
    path('demo/<int:id>', views.demo,name='demo'),
    path('cashWithdrawal', views.cashWithdrawal),
    path('cashWithdrawEntryValue',views.cashWithdrawEntryValue),
    path('cashDeposit',views.cashDeposit),
    path('cashDepositEntryValue',views.cashDepositEntryValue),
    path('sample_Excel',views.sample_Excel),
    path('download_excel_data',views.download_excel_data),
    path('export_csv',views.export_csv),
    path('demo/file_store',views.file_store,name="file_store"),
    path('destroyFile/<int:id>',views.destroyFile,name='deletefile'),
    path('showMembersDetails',views.showMembersDetails,name='showMembersDetails'),
    path('addnewMembersDetails',views.addnewMembersDetails),
    path('editMembersDetails/<int:id>',views.editMembersDetails),
    path('updateMembersDetails/<int:id>',views.updateMembersDetails),
    path('deletedMembersDetails/<int:id>',views.destroyMembersDetails),
    path('export_users_xlsImembersDetails',views.export_users_xlsImembersDetails),


    # path('showincome_expense_ledger2', views.showincome_expense_ledger2, name="showincome_expense_ledger2"),
]


if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)