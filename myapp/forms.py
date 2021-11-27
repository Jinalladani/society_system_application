from django import forms
from .models import ExpenseCategory, IncomeCategory, Income_Expense_LedgerValue1, BalanceValue, \
    Members_Vendor_Account, FileStoreValue1, MembersDeatilsValue


# class EmployeeForm(forms.ModelForm):
#     class Meta:
#         model = Employee
#         fields = ['name', 'contact', 'email', 'age']  # https://docs.djangoproject.com/en/3.0/ref/forms/widgets/
#         widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
#                    'email': forms.EmailInput(attrs={'class': 'form-control'}),
#                    'contact': forms.TextInput(attrs={'class': 'form-control'}),
#                    'age': forms.TextInput(attrs={'class': 'form-control'})}


class ExpensiveCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ['category_name']  # https://docs.djangoproject.com/en/3.0/ref/forms/widgets/
        widgets = {'category_name': forms.TextInput(attrs={'class': 'form-control'})
                   }


class IncomeCategoryForm(forms.ModelForm):
    class Meta:
        model = IncomeCategory
        fields = ['category_name']  # https://docs.djangoproject.com/en/3.0/ref/forms/widgets/
        widgets = {'category_name': forms.TextInput(attrs={'class': 'form-control'})
                   }


class Members_Vendor_AccountForm(forms.ModelForm):
    class Meta:
        model = Members_Vendor_Account
        fields = ['name']  # https://docs.djangoproject.com/en/3.0/ref/forms/widgets/
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})
                   }


class MembersDeatilsForm(forms.ModelForm):
    class Meta:
        model = MembersDeatilsValue
        fields = ['flatNo', 'primaryName', 'primaryContactNo', 'secondaryName', 'secondaryContactNo', 'accountingName',
                  'whatsappContactNo', 'email', 'residence']  # https://docs.djangoproject.com/en/3.0/ref/forms/widgets/
        widgets = {'flatNo': forms.TextInput(attrs={'class': 'form-control'}),
                   'primaryName': forms.TextInput(attrs={'class': 'form-control'}),
                   'primaryContactNo': forms.TextInput(attrs={'class': 'form-control'}),
                   'secondaryName': forms.TextInput(attrs={'class': 'form-control'}),
                   'secondaryContactNo': forms.TextInput(attrs={'class': 'form-control'}),
                   'accountingName': forms.TextInput(attrs={'class': 'form-control'}),
                   'whatsappContactNo': forms.TextInput(attrs={'class': 'form-control'}),
                   'email': forms.TextInput(attrs={'class': 'form-control'}),
                   'residence': forms.TextInput(attrs={'class': 'form-control'})
                   }


class BalanceFrom(forms.ModelForm):
    class Meta:
        model = BalanceValue
        fields = ['balance_amount']  # https://docs.djangoproject.com/en/3.0/ref/forms/widgets/
        widgets = {'balance_amount': forms.TextInput(attrs={'class': 'form-control'})
                   }


class Income_Expense_LedgerForm(forms.ModelForm):
    class Meta:
        model = Income_Expense_LedgerValue1
        fields = ['dateOn', 'type', 'amount', 'category_header', 'from_or_to_account', 'transaction_type',
                  'transaction_details',
                  'voucherNo_or_invoiceNo', 'remark', 'opening_balance_cash', 'closing_balance_cash',
                  'opening_balance_bank',
                  'closing_balance_bank']
        widgets = {'dateOn': forms.DateInput(attrs={'class': 'form-control'}),
                   'type': forms.TextInput(attrs={'class': 'form-control'}),
                   'amount': forms.TextInput(attrs={'class': 'form-control'}),
                   'category_header': forms.TextInput(attrs={'class': 'form-control'}),
                   'from_or_to_account': forms.TextInput(attrs={'class': 'form-control'}),
                   'transaction_type': forms.TextInput(attrs={'class': 'form-control'}),
                   'transaction_details': forms.TextInput(attrs={'class': 'form-control'}),
                   'voucherNo_or_invoiceNo': forms.TextInput(attrs={'class': 'form-control'}),
                   'remark': forms.Textarea(attrs={'class': 'form-control'}),
                   'opening_balance_cash': forms.TextInput(attrs={'class': 'form-control'}),
                   'closing_balance_cash': forms.TextInput(attrs={'class': 'form-control'}),
                   'opening_balance_bank': forms.TextInput(attrs={'class': 'form-control'}),
                   'closing_balance_bank': forms.TextInput(attrs={'class': 'form-control'}),
                   'entry_time': forms.DateInput(attrs={'class': 'form-control'})
                   }


class FileStoreForm(forms.ModelForm):
    class Meta:
        model = FileStoreValue1
        fields = ['text', 'type_file']  # https://docs.djangoproject.com/en/3.0/ref/forms/widgets/
        widgets = {'text': forms.TextInput(attrs={'class': 'form-control'}),
                   'type_file': forms.FileField()
                   }
