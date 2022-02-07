import csv
import requests
from random import randint
from django.core.mail import send_mail
from django.contrib import auth
from django.db.models import Sum
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from tablib import Dataset
from .models import ExpenseCategory, IncomeCategory, Income_Expense_LedgerValue1, \
    BalanceValue, \
    Members_Vendor_Account, FileStoreValue1, MembersDeatilsValue, Society, UserPermission, AssentCategory1, \
    Asset_InventoryCategoryValue1, AppData, MessageTemplate
from .resource import ExpenseResource, IncomeResource, Members_VendoorsResource, Income_Expense_LedgerResource, \
    MembersDetailsResource, AssentInventoryResource, AssentCategoryResource
from django.shortcuts import render, redirect
import xlwt
from django.http import HttpResponse
import datetime
from .check_me import check_user
from accounts.models import User
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from datetime import datetime, date
from django.http import JsonResponse

def index(request):
    balance = BalanceValue.objects.filter(society_key=request.user.userpermission.society_key)

    today_date = datetime.today()

    if request.method == 'POST':
        current_year = request.POST['datepicker']
    else:
        current_year = today_date.year

    contentBalance = {
        'balanceValue': balance
    }
    print(contentBalance)

    totalExpenseAmount = Income_Expense_LedgerValue1.objects.filter(society_key=request.user.userpermission.society_key,
                                                                    type='Expense').aggregate(Sum('amount'))
    print(totalExpenseAmount)

    totalIncomeAmount = Income_Expense_LedgerValue1.objects.filter(society_key=request.user.userpermission.society_key,
                                                                   type='Income').aggregate(
        Sum('amount'))
    print(totalIncomeAmount)

    listExpense = ExpenseCategory.objects.filter(society_key=request.user.userpermission.society_key)
    print(listExpense)

    expenseAmountSum = Income_Expense_LedgerValue1.objects.values('category_header').filter(
        society_key=request.user.userpermission.society_key, type='Expense').annotate(
        totalamount=Sum('amount'))
    print(expenseAmountSum)

    listIncome = IncomeCategory.objects.filter(society_key=request.user.userpermission.society_key)
    print(listIncome)

    incomeAmountSum = Income_Expense_LedgerValue1.objects.values('category_header').filter(
        society_key=request.user.userpermission.society_key, type='Income').annotate(
        totalamount=Sum('amount'))
    print(incomeAmountSum)

    topExpense = Income_Expense_LedgerValue1.objects.values('from_or_to_account', 'category_header',
                                                            'transaction_type', 'amount').filter(
        society_key=request.user.userpermission.society_key, type='Expense').order_by('amount').reverse()[0:20]
    print("---------topExpense-------------", topExpense)

    topIncome = Income_Expense_LedgerValue1.objects.values('from_or_to_account', 'category_header',
                                                           'transaction_type', 'amount').filter(
        society_key=request.user.userpermission.society_key, type='Income').order_by('amount').reverse()[0:20]
    print(topIncome)

    topMemberExpense = Income_Expense_LedgerValue1.objects.values('from_or_to_account').annotate(
        amount=Sum('amount')).filter(society_key=request.user.userpermission.society_key, type='Expense').order_by(
        'amount').reverse()[
                       0:20]

    topMemberIncome = Income_Expense_LedgerValue1.objects.values('from_or_to_account').annotate(
        amount=Sum('amount')).filter(society_key=request.user.userpermission.society_key, type='Income').order_by(
        'amount').reverse()[0:20]

    total_exp = []
    total_inco = []

    j = 1
    for i in range(12):
        totalExpense = Income_Expense_LedgerValue1.objects.filter(society_key=request.user.userpermission.society_key,
                                                                  type='Expense', dateOn__month=j,
                                                                  dateOn__year=current_year).aggregate(
            Sum('amount'))
        totalIncome = Income_Expense_LedgerValue1.objects.filter(society_key=request.user.userpermission.society_key,
                                                                 type='Income', dateOn__month=j,
                                                                 dateOn__year=current_year).aggregate(
            Sum('amount'))

        if totalExpense['amount__sum'] is None:
            total_exp.append(0)
        else:
            total_exp.append(totalExpense['amount__sum'])

        if totalIncome['amount__sum'] is None:
            total_inco.append(0)
        else:
            total_inco.append(totalIncome['amount__sum'])
        j += 1

    return render(request, 'index.html',
                  {'contentBalance': contentBalance, 'totalExpenseAmount': totalExpenseAmount,
                   'totalIncomeAmount': totalIncomeAmount,
                   'listExpense': listExpense, 'listIncome': listIncome, 'expenseAmountSum': expenseAmountSum,
                   'incomeAmountSum': incomeAmountSum, 'topExpense': topExpense, 'topIncome': topIncome,
                   'topMemberExpense': topMemberExpense, 'topMemberIncome': topMemberIncome,
                   'total_exp': total_exp,
                   'total_inco': total_inco,
                   'current_year': current_year,
                   })


def registrationpage(request):
    return render(request, 'registration.html')


def loginpage(request):
    return render(request, 'login.html')


def otpVerified(request):
    return render(request, 'otpVerified.html')


def upload_file(request):
    return render(request, 'upload.html')


def societyProfile(request):
    # societyDeatils = Society.objects.filter(society_key=request.user.userpermission.society_key)
    socDeatils = Society.objects.get(pk=request.user.userpermission.society_key.id)

    context = {
        'socDeatils': socDeatils
    }

    return render(request, 'societyProfile.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is None:
            message = "Enter Valid Data"
            data = {
                'message': message
            }
            return render(request, 'login.html', data)

        user_permission = UserPermission.objects.get(user_key=user)

        if user_permission:
            if user_permission.is_active and user_permission.is_member:
                return redirect('login')
            elif user_permission.is_active and user_permission.society_key.is_active:
                auth.login(request, user)
                return redirect('index')
            else:
                return redirect('login')
        else:
            if user:
                auth.login(request, user)
                return redirect('index')
            else:
                return redirect('login')

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = make_password(request.POST['password'])
        contact_name = request.POST['contact_name']
        phone_no = request.POST['phone_no']
        society_name = request.POST['society_name']
        society_address = request.POST['society_address']
        city = request.POST['city']
        pin_code = request.POST['pin_code']
        state = request.POST['state']
        country = request.POST['country']
        society_registration_number = request.POST['society_registration_number']
        uid = User.objects.create(email=email, password=password, phone_no=phone_no)

        society_name_data = Society.objects.filter(society_name__iexact=society_name)
        if society_name_data:
            message = "Please Change Your Society Name"
            return render(request, 'registration.html', {'message': message})
        else:
            society_obj = Society.objects.create(society_name=society_name, society_address=society_address,
                                                 city=city, pin_code=pin_code, state=state, country=country,
                                                 society_registration_number=society_registration_number,
                                                 contact_name=contact_name, email=email, phone_no=phone_no)

            UserPermission.objects.create(society_key=society_obj, user_key=uid, is_society_admin=True, is_active=True)

            return redirect('login')
    return render(request, 'registration.html')


def forgot_password(request):
    return render(request, 'forgot_password.html')


def send_otp(request):
    email = request.POST['email']
    generate_otp = randint(1111, 9999)
    uid = User.objects.filter(email=email)

    if uid:
        uid.update(otp=generate_otp)
        sendmail(" Forgot Password ", "mail_template", email, {'otp': generate_otp, 'uid': uid})
        return render(request, 'reset_password.html', {'email': email, 'otp': generate_otp})
    else:
        message = "Email does not exist"
        return render(request, 'forgot_password.html', {'message': message})


def sendmail(subject, template, to, context):
    email_user = AppData.objects.get(key="EMAIL_HOST_USER")
    email_password = AppData.objects.get(key="EMAIL_HOST_PASSWORD")

    EMAIL_HOST_USER = email_user
    EMAIL_HOST_PASSWORD = email_password
    template_str = template + '.html'
    html_message = render_to_string(template_str, {'data': context})
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, EMAIL_HOST_USER, [to], html_message=html_message)


def reset_password(request):
    try:
        email = request.POST['email']
        otp = request.POST['otp']
        otp1 = request.POST['otp1']
        password = request.POST['password']
        cpassword = request.POST['password']
        uid = User.objects.get(email=email)
        if uid:
            if otp1 == otp and password == cpassword:
                uid.password = make_password(password)
                uid.save()
                message = "password reset succesfully"
                return redirect('login')
            else:
                message = "invalid otp or password"
                return render(request, 'reset_password.html', {'message': message})
    except:
        message = "invalid Email"
        return render(request, 'login.html', {'message': message})


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect('login')


def ExpensiveCategory(request):
    print("allExpensiveCategory-----------")
    allExpensiveCategory = ExpenseCategory.objects.filter(society_key=request.user.userpermission.society_key)
    context = {
        'expensiveCategory': allExpensiveCategory
    }
    print(context)
    return render(request, 'ExpensiveCategory.html', context)


def addnewExpensiveCategory(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']

        ExpenseCategory.objects.create(category_name=category_name, society_key=request.user.userpermission.society_key)
        return redirect('ExpensiveCategory')

    return render(request, 'addExpensiveCategory.html')


def editExpensiveCategory(request, id):
    expensiveCategory = ExpenseCategory.objects.get(id=id)

    if request.method == 'POST':
        category_name = request.POST['category_name']
        expensiveCategory.category_name = category_name
        expensiveCategory.save()
        return redirect('ExpensiveCategory')

    return render(request, 'editExpensiveCategory.html', {'expensiveCategory': expensiveCategory})


def destroyExpensiveCategory(request, id):
    print("destroy expensive category-----------")
    expensiveCategory = ExpenseCategory.objects.get(id=id).delete()
    return redirect("ExpensiveCategory")


def multi_deleteExpenseCategory(request):
    print("Expense multi delete -------------")
    if request.method == "POST":
        product_ids = request.POST.getlist('id[]')
        print("delete this id ----------->", product_ids)
        for id in product_ids:
            expenseCtaegory = ExpenseCategory.objects.get(pk=id)
            expenseCtaegory.delete()
            print(" expenseCtaegory  delete this id ----------->", id)
        return redirect('ExpensiveCategory')


def all_deleteExpenseCategory(request):
    print("Expense multi delete -------------")
    if request.method == "POST":
        expenseCtaegory = ExpenseCategory.objects.filter(society_key=request.user.userpermission.society_key)
        expenseCtaegory.delete()
        print(" expenseCtaegory  delete this id ----------->")
        return redirect('ExpensiveCategory')


def IncomeCategoryshow(request):
    print("allIncomeCategory-----------")
    allIncomeCategory = IncomeCategory.objects.filter(society_key=request.user.userpermission.society_key)
    paginator = Paginator(allIncomeCategory, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'incomeCategory': page_obj
    }
    print(context)
    return render(request, 'incomeCategory.html', context)


def addnewIncomeCategory(request):
    print("add new Income Category--------------------")
    if request.method == 'POST':
        category_name = request.POST['category_name']

        IncomeCategory.objects.create(category_name=category_name, society_key=request.user.userpermission.society_key)
        return redirect('IncomeCategoryshow')

    return render(request, 'addIncomeCategory.html')


def editIncomeCategory(request, id):
    incomeCategory = IncomeCategory.objects.get(id=id)

    if request.method == 'POST':
        category_name = request.POST['category_name']
        incomeCategory.category_name = category_name
        incomeCategory.save()
        return redirect('IncomeCategoryshow')

    return render(request, 'editIncomeCategory.html', {'incomeCategory': incomeCategory})


def destroyIncomeCategory(request, id):
    print("destroy Income-----------")
    incomeCategory = IncomeCategory.objects.get(id=id)
    incomeCategory.delete()
    return redirect("IncomeCategoryshow")


def multi_deleteIncomeCategory(request):
    print("Income multi delete -------------")
    if request.method == "POST":
        product_ids = request.POST.getlist('id[]')
        print("delete this id ----------->", product_ids)
        for id in product_ids:
            incomeCtaegory = IncomeCategory.objects.get(pk=id)
            incomeCtaegory.delete()
            print(" IncomeCtaegory  delete this id ----------->", id)
        return redirect('IncomeCategoryshow')


def multipleSearch(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        ledgerobj = Income_Expense_LedgerValue1.objects.raw(
            'select * from myapp_income_expense_ledgervalue1 where type ="' + type + '"')
        return render(request, 'showIncome_expense_ledger.html', {'ledgerobj': ledgerobj})
    else:
        allincome_expense_ledger = Income_Expense_LedgerValue1.objects.all()
        return redirect('showIncome_expense_ledger')


def all_deleteIncomeCategory(request):
    print("Expense multi delete -------------")
    if request.method == "POST":
        incomeCtaegory = IncomeCategory.objects.filter(society_key=request.user.userpermission.society_key)
        incomeCtaegory.delete()
        print(" incomeCtaegory  delete this id ----------->")
        return redirect('IncomeCategoryshow')


def showincome_expense_ledger(request):
    if request.method == 'POST':
        dateOn = request.POST['from_date']
        to_date = request.POST['to_date']
        amount = request.POST['amount']
        type = request.POST['type']
        transaction_type = request.POST['transaction_type']
        category_header = request.POST['category_header']
        from_or_to_account = request.POST['from_or_to_account']
        voucherNo_or_invoiceNo = request.POST['voucherNo_or_invoiceNo']
        print('amount-------------', amount, type)
        allmembersValue = Members_Vendor_Account.objects.filter(society_key=request.user.userpermission.society_key)
        contextMember = {
            'memberValue': allmembersValue
        }
        print(contextMember)

        if to_date == "":
            to_date = dateOn
        income_expense_ledger = Income_Expense_LedgerValue1.objects.filter(
            society_key=request.user.userpermission.society_key)

        if dateOn != '' and to_date != '':
            income_expense_ledger = income_expense_ledger.filter(dateOn__range=[dateOn, to_date])
        if transaction_type != "NULL":
            income_expense_ledger = income_expense_ledger.filter(transaction_type=transaction_type)
        if amount != "":
            income_expense_ledger = income_expense_ledger.filter(amount=amount)
        if type != "NULL":
            income_expense_ledger = income_expense_ledger.filter(type=type)
        if category_header != "":
            income_expense_ledger = income_expense_ledger.filter(category_header=category_header)
        if from_or_to_account != "NULL":
            income_expense_ledger = income_expense_ledger.filter(from_or_to_account=from_or_to_account)
        if voucherNo_or_invoiceNo != "":
            income_expense_ledger = income_expense_ledger.filter(voucherNo_or_invoiceNo=voucherNo_or_invoiceNo)
        print(income_expense_ledger)

        if 'export' in request.POST:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=ledger' + str(datetime.datetime.now()) + '.csv'

            writer = csv.writer(response)
            writer.writerow(
                ['id', 'dateOn', 'type', 'amount', 'category_header', 'from_or_to_account', 'transaction_type',
                 'transaction_details', 'voucherNo_or_invoiceNo', 'remark', 'opening_balance_cash',
                 'closing_balance_cash',
                 'opening_balance_bank', 'closing_balance_bank',
                 'entry_time'])

            valuestore = income_expense_ledger

            for exp in valuestore:
                writer.writerow([exp.id, exp.dateOn, exp.type, exp.amount, exp.category_header, exp.from_or_to_account,
                                 exp.transaction_type,
                                 exp.transaction_details, exp.voucherNo_or_invoiceNo, exp.remark,
                                 exp.opening_balance_cash,
                                 exp.closing_balance_cash, exp.opening_balance_bank, exp.closing_balance_bank,
                                 exp.entry_time])

            return response

        return render(request, 'showIncome_expense_ledger.html',
                      {'income_expense_ledger': income_expense_ledger, 'contextMember': contextMember, 'type': type,
                       'dateOn': dateOn, 'to_date': to_date, 'amount': amount, 't_type': transaction_type,
                       'c_header': category_header,
                       's_member': from_or_to_account, 'v_number': voucherNo_or_invoiceNo})
    else:
        print("allincome_expense_ledger-----------")
        allincome_expense_ledger = Income_Expense_LedgerValue1.objects.filter(
            society_key=request.user.userpermission.society_key)
        # paginator = Paginator(allincome_expense_ledger, 10)
        # page_number = request.GET.get('page')
        # page_obj = paginator.get_page(page_number)

        context = {
            'income_expense_ledger': allincome_expense_ledger
        }
        print(context)
        return render(request, 'showIncome_expense_ledger.html', context)


def addincome_expense_ledger(request):
    print("add  Income_expense_ledger Category--------------------")
    allexpValue = ExpenseCategory.objects.filter(society_key=request.user.userpermission.society_key)
    context = {
        'expValue': allexpValue
    }
    print(context)
    allincValue = IncomeCategory.objects.filter(society_key=request.user.userpermission.society_key)
    contextIncome = {
        'incValue': allincValue
    }
    print(contextIncome)
    allmembersValue = Members_Vendor_Account.objects.filter(society_key=request.user.userpermission.society_key)
    contextMember = {
        'memberValue': allmembersValue
    }
    print(contextMember)
    return render(request, 'addincome_expense_ledger.html',
                  {'context': context, 'contextIncome': contextIncome, 'contextMember': contextMember})


def income_expense_ledgerValue(request):
    date = request.POST['date']
    category = request.POST['category']
    amount = request.POST['amount']
    expense_value = request.POST['expense_value']
    income_value = request.POST['income_value']
    members_value = request.POST['members_value']
    transaction_type = request.POST['transaction_type']
    transaction_details = request.POST['transaction_details']
    voucherNo_or_invoiceNo = request.POST['voucherNo_or_invoiceNo']
    remark = request.POST['remark']
    obc = request.POST['obc']
    cbc = request.POST['cbc']
    obb = request.POST['obb']
    cbb = request.POST['cbb']
    entry_time = request.POST['entry_time']

    amount1 = float(amount)
    balance_set = BalanceValue.objects.filter(society_key=request.user.userpermission.society_key, account='Cash')
    print("balance ------------>", balance_set)
    for balance in balance_set:
        bal_amount = float(balance.balance_amount)
    print('bal_amount------', bal_amount)
    obc = bal_amount
    cbc = obc

    balance_set = BalanceValue.objects.filter(society_key=request.user.userpermission.society_key, account='Bank')
    print("balance ------------>", balance_set)
    for balance in balance_set:
        bal_amountBank = float(balance.balance_amount)

    print('bal_amount------', bal_amountBank)
    obb = bal_amountBank
    cbb = obb

    print("opening balace cash------", obc)
    print("closing balace cash------", cbc)
    print("opening balace Bank------", obb)
    print("closing balace Bank------", cbc)

    if transaction_type == 'Cash':
        if category == 'Expense':
            cbc = obc - amount1
        else:
            cbc = obc + amount1
    else:
        if category == 'Expense':
            cbb = obb - amount1
        else:
            cbb = obb + amount1

    if category == 'Expense':
        comCategory = expense_value
    else:
        comCategory = income_value

    if category == 'CASH WITHDRAWAL':
        bal_amtWithdrawBank = bal_amountBank - amount1
        obc = bal_amount
        obb = bal_amountBank
        cbc = bal_amount
        cbb = bal_amtWithdrawBank
        print('cash withdraw')
        print("---------------------- obc ", obc)
        print("----------------------obb ", obb)
        print("----------------------cbc ", cbc)
        print("----------------------cbb ", cbb)

    if category == 'CASH DEPOSIT':
        bal_amtWithdrawBank = bal_amountBank + amount1
        obc = bal_amount
        obb = bal_amountBank
        cbc = bal_amount
        cbb = bal_amtWithdrawBank
        print("deposite")
        print("---------------------- obc ", obc)
        print("----------------------obb ", obb)
        print("----------------------cbc ", cbc)
        print("----------------------cbb ", cbb)

    if category == 'CASH IN':
        bal_amtWithdrawCash = bal_amount + amount1
        obc = bal_amount
        obb = bal_amountBank
        cbc = bal_amtWithdrawCash
        cbb = bal_amountBank
        print("cash in")
        print("---------------------- obc ", obc)
        print("----------------------obb ", obb)
        print("----------------------cbc ", cbc)
        print("----------------------cbb ", cbb)

    if category == 'CASH OUT':
        bal_amtWithdrawCash = bal_amount - amount1
        obc = bal_amount
        obb = bal_amountBank
        cbc = bal_amtWithdrawCash
        cbb = bal_amountBank
        print("cash out")
        print("---------------------- obc ", obc)
        print("----------------------obb ", obb)
        print("----------------------cbc ", cbc)
        print("----------------------cbb ", cbb)

    entry_time = datetime.now()

    uid = Income_Expense_LedgerValue1.objects.create(dateOn=date, type=category, amount=amount,
                                                     category_header=comCategory,
                                                     from_or_to_account=members_value,
                                                     transaction_type=transaction_type,
                                                     transaction_details=transaction_details,
                                                     voucherNo_or_invoiceNo=voucherNo_or_invoiceNo,
                                                     remark=remark,
                                                     opening_balance_cash=obc, closing_balance_cash=cbc,
                                                     opening_balance_bank=obb,
                                                     closing_balance_bank=cbb, entry_time=entry_time,
                                                     society_key=request.user.userpermission.society_key)
    print(uid)
    updateBalanceValue(cbc, cbb, request)
    return redirect('showincome_expense_ledger')


def updateBalanceValue(cbc, cbb, request):
    caseObject = BalanceValue.objects.get(society_key=request.user.userpermission.society_key, account='Cash')
    print("cbc -------------", cbc)
    print(caseObject)
    caseObject.balance_amount = cbc
    caseObject.save()
    bankObject = BalanceValue.objects.get(society_key=request.user.userpermission.society_key, account='Bank')
    print('cbb--------------', cbb)
    print(bankObject)
    bankObject.balance_amount = cbb
    bankObject.save()


def cashWithdrawal(request):
    return render(request, 'cashWithdrawal.html')


def cashWithdrawEntryValue(request):
    date = request.POST['date']
    type = request.POST['type']
    amount = request.POST['amount']
    transaction_details = request.POST['transaction_details']
    obc = request.POST['obc']
    cbc = request.POST['cbc']
    obb = request.POST['obb']
    cbb = request.POST['cbb']
    entry_time = request.POST['entry_time']
    entry_time = datetime.now()

    amount1 = float(amount)
    balance_set = BalanceValue.objects.filter(society_key=request.user.userpermission.society_key, account='Cash')
    print("balance ------------>", balance_set)
    for balance in balance_set:
        bal_amount = float(balance.balance_amount)
    print('bal_amount------', bal_amount)
    obc = bal_amount
    cbc = obc

    balance_set = BalanceValue.objects.filter(society_key=request.user.userpermission.society_key, account='Bank')
    print("balance ------------>", balance_set)
    for balance in balance_set:
        bal_amountBank = float(balance.balance_amount)

    print('bal_amount------', bal_amountBank)
    obb = bal_amountBank
    cbb = obb

    cbb = obb - amount1
    transaction_type = 'Bank'
    from_or_to_account = 'Cash'
    bankBalanceChange = Income_Expense_LedgerValue1.objects.create(dateOn=date, type=type, amount=amount,
                                                                   from_or_to_account=from_or_to_account,
                                                                   transaction_type=transaction_type,
                                                                   transaction_details=transaction_details,
                                                                   opening_balance_cash=obc,
                                                                   closing_balance_cash=cbc,
                                                                   opening_balance_bank=obb,
                                                                   closing_balance_bank=cbb,
                                                                   entry_time=entry_time,
                                                                   society_key=request.user.userpermission.society_key)
    updateBalanceValue(cbc, cbb, request)
    balance_set = BalanceValue.objects.filter(society_key=request.user.userpermission.society_key, account='Bank')
    print("balance ------------>", balance_set)
    for balance in balance_set:
        bal_amountBank = float(balance.balance_amount)

    print('bal_amount------', bal_amountBank)
    obb = bal_amountBank
    cbb = obb

    cbc = obc + amount1
    transaction_type = 'Cash'
    from_or_to_account = 'Bank'
    cashBalanceChange = Income_Expense_LedgerValue1.objects.create(dateOn=date, type='CASH IN', amount=amount,
                                                                   from_or_to_account=from_or_to_account,
                                                                   transaction_type=transaction_type,
                                                                   transaction_details=transaction_details,
                                                                   opening_balance_cash=obc,
                                                                   closing_balance_cash=cbc,
                                                                   opening_balance_bank=obb,
                                                                   closing_balance_bank=cbb,
                                                                   entry_time=entry_time,
                                                                   society_key=request.user.userpermission.society_key)
    updateBalanceValue(cbc, cbb, request)
    return redirect('showincome_expense_ledger')


def cashDeposit(request):
    return render(request, 'cashDeposit.html')


def cashDepositEntryValue(request):
    date = request.POST['date']
    type = request.POST['type']
    amount = request.POST['amount']
    transaction_details = request.POST['transaction_details']
    obc = request.POST['obc']
    cbc = request.POST['cbc']
    obb = request.POST['obb']
    cbb = request.POST['cbb']
    entry_time = request.POST['entry_time']
    entry_time = datetime.now()

    amount1 = float(amount)
    balance_set = BalanceValue.objects.filter(society_key=request.user.userpermission.society_key, account='Cash')
    print("balance ------------>", balance_set)
    bal_amount = 0
    for balance in balance_set:
        bal_amount = float(balance.balance_amount)
    print('bal_amount------', bal_amount)
    obc = bal_amount
    cbc = obc

    balance_set = BalanceValue.objects.filter(society_key=request.user.userpermission.society_key, account='Bank')
    print("balance ------------>", balance_set)
    for balance in balance_set:
        bal_amountBank = float(balance.balance_amount)

    print('bal_amount------', bal_amountBank)
    obb = bal_amountBank
    cbb = obb

    cbc = obc - amount1
    transaction_type = 'Cash'
    from_or_to_account = 'Bank'
    cashBalanceChange = Income_Expense_LedgerValue1.objects.create(dateOn=date, type='CASH OUT', amount=amount,
                                                                   from_or_to_account=from_or_to_account,
                                                                   transaction_type=transaction_type,
                                                                   transaction_details=transaction_details,
                                                                   opening_balance_cash=obc,
                                                                   closing_balance_cash=cbc,
                                                                   opening_balance_bank=obb,
                                                                   closing_balance_bank=cbb,
                                                                   entry_time=entry_time,
                                                                   society_key=request.user.userpermission.society_key)
    updateBalanceValue(cbc, cbb, request)
    balance_set = BalanceValue.objects.filter(society_key=request.user.userpermission.society_key, account='Cash')
    print("balance ------------>", balance_set)
    for balance in balance_set:
        bal_amount = float(balance.balance_amount)
    print('bal_amount------', bal_amount)
    obc = bal_amount
    cbc = obc

    cbb = obb + amount1
    transaction_type = 'Bank'
    from_or_to_account = 'Cash'
    bankBalanceChange = Income_Expense_LedgerValue1.objects.create(dateOn=date, type=type, amount=amount,
                                                                   from_or_to_account=from_or_to_account,
                                                                   transaction_type=transaction_type,
                                                                   transaction_details=transaction_details,
                                                                   opening_balance_cash=obc,
                                                                   closing_balance_cash=cbc,
                                                                   opening_balance_bank=obb,
                                                                   closing_balance_bank=cbb,
                                                                   entry_time=entry_time,
                                                                   society_key=request.user.userpermission.society_key)
    updateBalanceValue(cbc, cbb, request)
    return redirect('showincome_expense_ledger')


def editIncome_expense_ledger(request, id):
    print("editIncome_expense_ledger ------------")
    income_expense_ledger = Income_Expense_LedgerValue1.objects.get(id=id)
    print(income_expense_ledger.dateOn)
    if income_expense_ledger.type == 'Expense':
        type_headerList = ExpenseCategory.objects.all()
    elif income_expense_ledger.type == 'Income':
        type_headerList = IncomeCategory.objects.all()
    else:
        type_headerList = 'NULL'
    print(type_headerList)

    if request.method == 'POST':
        dateOn = request.POST['date']
        print(dateOn)
        type = request.POST['type']
        amount = request.POST['amount']
        category_header = request.POST['category_header']
        from_or_to_account = request.POST['from_or_to_account']
        transaction_type = request.POST['transaction_type']
        transaction_details = request.POST['transaction_details']
        voucherNo_or_invoiceNo = request.POST['voucherNo_or_invoiceNo']
        remark = request.POST['remark']
        income_expense_ledger.dateOn = dateOn
        income_expense_ledger.type = type
        income_expense_ledger.amount = amount
        income_expense_ledger.category_header = category_header
        income_expense_ledger.from_or_to_account = from_or_to_account
        income_expense_ledger.transaction_type = transaction_type
        income_expense_ledger.transaction_details = transaction_details
        income_expense_ledger.voucherNo_or_invoiceNo = voucherNo_or_invoiceNo
        income_expense_ledger.remark = remark
        income_expense_ledger.save()
        return redirect('showincome_expense_ledger')

    return render(request, 'editIncome_expense_ledger.html',
                  {'income_expense_ledger': income_expense_ledger, 'type_headerList': type_headerList})


def destroyIncome_expense_ledger(request, id):
    print("destroyIncome_expense_ledger-----------")
    income_expense_ledger = Income_Expense_LedgerValue1.objects.get(id=id)
    income_expense_ledger.delete()
    return redirect("showincome_expense_ledger")


def multi_deleteIncome_Expense_Ledger(request):
    print("post delete -------------")
    if request.method == "POST":
        product_ids = request.POST.getlist('id[]')
        print("delete this id ----------->", product_ids)
        for id in product_ids:
            employee = Income_Expense_LedgerValue1.objects.get(pk=id)
            employee.delete()
            print(" employe  delete this id ----------->", id)
        return redirect('showincome_expense_ledger')


def all_deleteIncome_Expense_Ledger(request):
    print("income_expense_ledger all delete -------------")
    if request.method == "POST":
        income_expense_ledger = Income_Expense_LedgerValue1.objects.filter(
            society_key=request.user.userpermission.society_key)
        income_expense_ledger.delete()
        print(" income_expense_ledger  delete this id ----------->")
        return redirect('showincome_expense_ledger')


def showBalance(request):
    print("all Balance-----------")
    allBalance = BalanceValue.objects.filter(society_key=request.user.userpermission.society_key)
    context = {
        'balance': allBalance
    }
    print(context)
    return render(request, 'showBalance.html', context)


def addnewBalance(request):
    print("add new Balance--------------------")
    if request.method == 'POST':
        account = request.POST['type']
        balance_amount = request.POST['balnce_amount']
        data = BalanceValue.objects.filter(society_key=request.user.userpermission.society_key, account__iexact=account)
        if data:
            print("already there")
        else:
            BalanceValue.objects.create(society_key=request.user.userpermission.society_key, account=account,
                                        balance_amount=balance_amount)
        return redirect('showBalance')

    return render(request, 'addBalance.html')


def editBalance(request, id):
    balancecategory = BalanceValue.objects.get(id=id)

    if request.method == 'POST':
        account = request.POST['account']
        balance_amount = request.POST['balance_amount']
        balancecategory.account = account
        balancecategory.balance_amount = balance_amount
        balancecategory.save()
        return redirect('showBalance')

    return render(request, 'editBalance.html', {'balancecategory': balancecategory})


def destroyBalance(request, id):
    print("destroy Balance-----------")
    balance = BalanceValue.objects.get(id=id)
    balance.delete()
    return redirect("showBalance")


def showMembers_vendor(request):
    print("show Members_vendor-----------")
    allMembers_vendor = Members_Vendor_Account.objects.filter(society_key=request.user.userpermission.society_key)
    context = {
        'members_vendor': allMembers_vendor
    }
    print(context)
    return render(request, 'showMembers_vendor.html', context)


def addnewMembers_vendor(request):
    print("add new Members_vendor--------------------")
    if request.method == 'POST':
        name = request.POST['name']
        Members_Vendor_Account.objects.create(name=name, society_key=request.user.userpermission.society_key)
        return redirect('showMembers_vendor')
    return render(request, 'addMembers_vendor.html')


def editMembers_vendor(request, id):
    membersVendor = Members_Vendor_Account.objects.get(id=id)

    if request.method == 'POST':
        name = request.POST['name']
        membersVendor.name = name
        membersVendor.save()
        return redirect('showMembers_vendor')

    return render(request, 'editMembers_vendor.html', {'membersVendor': membersVendor})


def destroyMembers_vendor(request, id):
    print("destroy  membersVendor-----------")
    membersVendor = Members_Vendor_Account.objects.get(id=id)
    membersVendor.delete()
    return redirect("showMembers_vendor")


def multi_deleteMembers_vendor(request):
    print("Member-vendor multi delete -------------")
    if request.method == "POST":
        product_ids = request.POST.getlist('id[]')
        print("delete this id ----------->", product_ids)
        for id in product_ids:
            member_vendor = Members_Vendor_Account.objects.get(pk=id)
            member_vendor.delete()
            print(" IncomeCtaegory  delete this id ----------->", id)
        return redirect('showMembers_vendor')


def all_deleteMembers_vendor(request):
    print("Members_vendor all delete -------------")
    if request.method == "POST":
        member_vendor = Members_Vendor_Account.objects.filter(
            society_key=request.user.userpermission.society_key)
        member_vendor.delete()
        print(" Members_vendor  delete this id ----------->")
        return redirect('showMembers_vendor')


def showMembersDetails(request):
    print("show MembersDetails-----------")
    allMembersDetails = MembersDeatilsValue.objects.filter(society_key=request.user.userpermission.society_key)
    context = {
        'membersMembersDetails': allMembersDetails
    }
    print(context)
    return render(request, 'showMembersDetails.html', context)


def addnewMembersDetails(request):
    print("add new Members Details--------------------")
    if request.method == 'POST':
        flatNo = request.POST['flatNo']
        primaryName = request.POST['primaryName']
        primaryContactNo = request.POST['primaryContactNo']
        secondaryName = request.POST['secondaryName']
        secondaryContactNo = request.POST['secondaryContactNo']
        accountingName = request.POST['accountingName']
        whatsappContactNo = request.POST['whatsappContactNo']
        email = request.POST['email']
        residence = request.POST['residence']

        MembersDeatilsValue.objects.create(flatNo=flatNo, primaryName=primaryName, primaryContactNo=primaryContactNo,
                                           secondaryName=secondaryName, secondaryContactNo=secondaryContactNo,
                                           accountingName=accountingName,
                                           whatsappContactNo=whatsappContactNo, email=email, residence=residence,
                                           society_key=request.user.userpermission.society_key)
        return redirect('showMembersDetails')
    return render(request, 'addMemberDetails.html')


def editMembersDetails(request, id):
    membersDetails = MembersDeatilsValue.objects.get(id=id)

    if request.method == 'POST':
        flatNo = request.POST['flatNo']
        primaryName = request.POST['primaryName']
        primaryContactNo = request.POST['primaryContactNo']
        secondaryName = request.POST['secondaryName']
        secondaryContactNo = request.POST['secondaryContactNo']
        accountingName = request.POST['accountingName']
        whatsappContactNo = request.POST['whatsappContactNo']
        email = request.POST['email']
        residence = request.POST['residence']

        membersDetails.flatNo = flatNo
        membersDetails.primaryName = primaryName
        membersDetails.primaryContactNo = primaryContactNo
        membersDetails.secondaryName = secondaryName
        membersDetails.secondaryContactNo = secondaryContactNo
        membersDetails.accountingName = accountingName
        membersDetails.whatsappContactNo = whatsappContactNo
        membersDetails.email = email
        membersDetails.residence = residence
        membersDetails.save()
        return redirect('showMembersDetails')

    return render(request, 'editMembersDetails.html', {'membersDetails': membersDetails})


def destroyMembersDetails(request, id):
    print("destroy  members Details-----------")
    membersDetails = MembersDeatilsValue.objects.get(id=id)
    membersDetails.delete()
    return redirect("showMembersDetails")


def multi_deleteMembersDetails(request):
    print("Member  multi delete -------------")
    if request.method == "POST":
        product_ids = request.POST.getlist('id[]')
        print("delete this id ----------->", product_ids)
        for id in product_ids:
            membersDetails = MembersDeatilsValue.objects.get(pk=id)
            membersDetails.delete()
            print(" membersDetails  delete this id ----------->", id)
        return redirect('showMembersDetails')


def all_deleteMembers(request):
    print("MembersDetails all delete -------------")
    if request.method == "POST":
        membersDetails = MembersDeatilsValue.objects.filter(
            society_key=request.user.userpermission.society_key)
        membersDetails.delete()
        print(" MembersDetails  delete this id ----------->")
        return redirect('showMembersDetails')


def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="expense.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('ExpenseCategory')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id', 'category_name']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = ExpenseCategory.objects.filter(society_key=request.user.userpermission.society_key).values_list('id',
                                                                                                           'category_name')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def export_users_xlsImcome(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="income.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('ImcomeCategory')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id', 'category_name']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = IncomeCategory.objects.filter(society_key=request.user.userpermission.society_key).values_list('id',
                                                                                                          'category_name')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def export_users_xlsImembers(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="members-vendors.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('members-vendors')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id', 'category_name']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Members_Vendor_Account.objects.filter(society_key=request.user.userpermission.society_key).values_list('id',
                                                                                                                  'name')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def export_users_xlsImembersDetails(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="membersDetails.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('membersDetails')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id', 'flatNo', 'primaryName', 'primaryContactNo', 'secondaryName', 'secondaryContactNo',
               'accountingName', 'whatsappContactNo', 'email', 'residence']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = MembersDeatilsValue.objects.filter(society_key=request.user.userpermission.society_key).values_list('id',
                                                                                                               'flatNo',
                                                                                                               'primaryName',
                                                                                                               'primaryContactNo',
                                                                                                               'secondaryName',
                                                                                                               'secondaryContactNo',
                                                                                                               'accountingName',
                                                                                                               'whatsappContactNo',
                                                                                                               'email',
                                                                                                               'residence')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def export_users_xlsLedger(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="ledger.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Income-Expense-Ledger')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id', 'dateOn', 'type', 'amount', 'category_header', 'from_or_to_account', 'transaction_type',
               'transaction_details', 'voucherNo_or_invoiceNo', 'remark', 'opening_balance_cash',
               'closing_balance_cash',
               'opening_balance_bank', 'closing_balance_bank']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Income_Expense_LedgerValue1.objects.filter(society_key=request.user.userpermission.society_key).values_list(
        'id', 'dateOn',
        'type', 'amount',
        'category_header',
        'from_or_to_account',
        'transaction_type',
        'transaction_details',
        'voucherNo_or_invoiceNo',
        'remark',
        'opening_balance_cash',
        'closing_balance_cash',
        'opening_balance_bank',
        'closing_balance_bank')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
        print(row)

    wb.save(response)
    return response


def simple_upload(request):
    if request.method == 'POST':
        emp_resource = ExpenseResource()
        dataset = Dataset()
        new_income = request.FILES['myfile']

        imported_data = dataset.load(new_income.read(), format='xlsx')
        for data in imported_data:
            ExpenseCategory.objects.create(society_key=request.user.userpermission.society_key, category_name=data[0])
        return redirect('ExpensiveCategory')


def simple_uploadIncome(request):
    if request.method == 'POST':
        emp_resource = ExpenseResource()
        dataset = Dataset()
        new_expense = request.FILES['myfile']

        imported_data = dataset.load(new_expense.read(), format='xlsx')
        for data in imported_data:
            IncomeCategory.objects.create(society_key=request.user.userpermission.society_key, category_name=data[0])

        return redirect('IncomeCategoryshow')


def simple_uploadMembers_Vendors(request):
    if request.method == 'POST':
        emp_resource = Members_VendoorsResource()
        dataset = Dataset()
        new_members = request.FILES['myfile']

        imported_data = dataset.load(new_members.read(), format='xlsx')
        for data in imported_data:
            Members_Vendor_Account.objects.create(society_key=request.user.userpermission.society_key, name=data[0])

        return redirect('showMembers_Vendor')


def simple_uploadMembersDetails(request):
    if request.method == 'POST':
        emp_resource = MembersDetailsResource()
        dataset = Dataset()
        new_members = request.FILES['myfile']

        imported_data = dataset.load(new_members.read(), format='xlsx')
        for data in imported_data:
            MembersDeatilsValue.objects.create(society_key=request.user.userpermission.society_key, flatNo=data[0],
                                               primaryName=data[1],
                                               primaryContactNo=data[2], secondaryName=data[3],
                                               secondaryContactNo=data[4], accountingName=data[5],
                                               whatsappContactNo=data[6], email=data[7],
                                               residence=data[8])
        return redirect('showMembersDetails')


def simple_uploadIncome_Expense_Ledger(request):
    if request.method == 'POST':
        emp_resource = Income_Expense_LedgerResource()
        dataset = Dataset()
        new_income = request.FILES['myfile']

        imported_data = dataset.load(new_income.read(), format='xlsx')

        data_range = 0
        for data_col in imported_data['date']:
            if data_col is None:
                break
            else:
                data_range += 1

        data = imported_data

        excelValue = []
        for data_obj in range(data_range):
            value = Income_Expense_LedgerValue1.objects.create(
                society_key=request.user.userpermission.society_key,
                dateOn=data[data_obj][0],
                type=data[data_obj][1],
                amount=data[data_obj][2],
                category_header=data[data_obj][3],
                from_or_to_account=data[data_obj][4],
                transaction_type=data[data_obj][5],
                transaction_details=data[data_obj][6],
                voucherNo_or_invoiceNo=data[data_obj][7],
                remark=data[data_obj][8],
            )

            excelValue.append(value)

        for valueUpdate in excelValue:
            print("--------------date ", valueUpdate.dateOn)
            print("-------------- list", valueUpdate.type)
            print("-------------- list amount", valueUpdate.amount)
            print("------------category header", valueUpdate.category_header)
            print('-------------- members ', valueUpdate.from_or_to_account)
            print("-----------transtion type", valueUpdate.transaction_type)
            print("-----------transtion details", valueUpdate.transaction_details)
            print("----------- voucher no", valueUpdate.voucherNo_or_invoiceNo)
            print("----------- remark", valueUpdate.remark)
            print("-------------- obc", valueUpdate.opening_balance_cash)
            print("-------------- cbc", valueUpdate.closing_balance_cash)
            print("-------------- obb", valueUpdate.opening_balance_bank)
            print("-------------- cbb", valueUpdate.closing_balance_bank)
            print("-----------------Entry date", valueUpdate.entry_time)
            print("--------------------------------------------------------------")

            amount1 = float(valueUpdate.amount)

            balance_set = BalanceValue.objects.get(society_key=request.user.userpermission.society_key, account='Cash')
            bal_amount = float(balance_set.balance_amount)

            valueUpdate.opening_balance_cash = bal_amount
            valueUpdate.closing_balance_cash = valueUpdate.opening_balance_cash

            balance_set = BalanceValue.objects.get(society_key=request.user.userpermission.society_key, account='Bank')
            bal_amountBank = float(balance_set.balance_amount)
            valueUpdate.opening_balance_bank = bal_amountBank
            valueUpdate.closing_balance_bank = valueUpdate.opening_balance_bank

            if valueUpdate.transaction_type == 'Cash':
                if valueUpdate.type == 'Expense':
                    valueUpdate.closing_balance_cash = valueUpdate.opening_balance_cash - amount1
                else:
                    valueUpdate.closing_balance_cash = valueUpdate.opening_balance_cash + amount1
            else:
                if valueUpdate.type == 'Expense':
                    valueUpdate.closing_balance_bank = valueUpdate.opening_balance_bank - amount1
                else:
                    valueUpdate.closing_balance_bank = valueUpdate.opening_balance_bank + amount1

            if valueUpdate.type == 'CASH WITHDRAWAL':
                bal_amtWithdrawBank = valueUpdate.opening_balance_bank - amount1
                valueUpdate.opening_balance_cash = bal_amount
                valueUpdate.opening_balance_bank = bal_amountBank
                valueUpdate.closing_balance_cash = bal_amount
                valueUpdate.closing_balance_bank = bal_amtWithdrawBank

            if valueUpdate.type == 'CASH DEPOSIT':
                bal_amtWithdrawBank = valueUpdate.opening_balance_bank + amount1
                valueUpdate.opening_balance_cash = bal_amount
                valueUpdate.opening_balance_bank = bal_amountBank
                valueUpdate.closing_balance_cash = bal_amount
                valueUpdate.closing_balance_bank = bal_amtWithdrawBank

            if valueUpdate.type == 'CASH IN':
                bal_amtWithdrawCash = valueUpdate.opening_balance_cash + amount1
                valueUpdate.opening_balance_cash = bal_amount
                valueUpdate.opening_balance_bank = bal_amountBank
                valueUpdate.closing_balance_cash = bal_amtWithdrawCash
                valueUpdate.closing_balance_bank = bal_amountBank

            if valueUpdate.type == 'CASH OUT':
                bal_amtWithdrawCash = valueUpdate.opening_balance_cash - amount1
                valueUpdate.opening_balance_cash = bal_amount
                valueUpdate.opening_balance_bank = bal_amountBank
                valueUpdate.closing_balance_cash = bal_amtWithdrawCash
                valueUpdate.closing_balance_bank = bal_amountBank

            valueUpdate.entry_time = datetime.now()

            if Members_Vendor_Account.objects.filter(name__icontains=valueUpdate.from_or_to_account,
                                                     society_key=request.user.userpermission.society_key):
                print("record found")
            else:
                print("record not found")
                checkmember = Members_Vendor_Account.objects.create(name=valueUpdate.from_or_to_account,
                                                                    society_key=request.user.userpermission.society_key)

            if valueUpdate.type == 'Expense':
                if ExpenseCategory.objects.filter(category_name__icontains=valueUpdate.category_header,
                                                  society_key=request.user.userpermission.society_key):
                    print("record found")
                else:
                    print("record not found")
                    checkexpense = ExpenseCategory.objects.create(category_name=valueUpdate.category_header,
                                                                  society_key=request.user.userpermission.society_key)

            if valueUpdate.type == 'Income':
                if IncomeCategory.objects.filter(category_name__icontains=valueUpdate.category_header,
                                                 society_key=request.user.userpermission.society_key):
                    print("record found")
                else:
                    print("record not found")
                    checkexpense = IncomeCategory.objects.create(category_name=valueUpdate.category_header,
                                                                 society_key=request.user.userpermission.society_key)

            print("-------------update value-date ", valueUpdate.dateOn)
            print("-------------- list", valueUpdate.type)
            print("-------------- list amount", valueUpdate.amount)
            print("------------category header", valueUpdate.category_header)
            print('-------------- members ', valueUpdate.from_or_to_account)
            print("-----------transtion type", valueUpdate.transaction_type)
            print("-----------transtion details", valueUpdate.transaction_details)
            print("----------- voucher no", valueUpdate.voucherNo_or_invoiceNo)
            print("----------- remark", valueUpdate.remark)
            print("---------update value----- obc", valueUpdate.opening_balance_cash)
            print("---------update value----- cbc", valueUpdate.closing_balance_cash)
            print("---------update value----- obb", valueUpdate.opening_balance_bank)
            print("---------update value----- cbb", valueUpdate.closing_balance_bank)
            print("-----------------Entry date", valueUpdate.entry_time)
            print("--------------------------------------------------------------")
            print("--------------------------------------------------------------")
            print("--------------------------------------------------------------")

            valueUpdate.save()
            updateBalanceValueUploadFile(valueUpdate.closing_balance_cash
                                         , valueUpdate.closing_balance_bank, request)
        value.save()

    return redirect('showincome_expense_ledger')


def updateBalanceValueUploadFile(cbc, cbb, request):
    caseObject = BalanceValue.objects.get(account='Cash', society_key=request.user.userpermission.society_key)
    print("cbc -------------", cbc)
    print(caseObject)
    caseObject.balance_amount = cbc
    caseObject.save()
    bankObject = BalanceValue.objects.get(account='Bank', society_key=request.user.userpermission.society_key)
    print('cbb--------------', cbb)
    print(bankObject)
    bankObject.balance_amount = cbb
    bankObject.save()


def sample_Excel(request):
    expensList = ExpenseCategory.objects.all()
    return render(request, 'sample_Excel.html', {'expensList': expensList})


def download_excel_data(request):
    # content-type of response
    response = HttpResponse(content_type='application/ms-excel')

    # decide file name
    response['Content-Disposition'] = 'attachment; filename="ThePythonDjango.xls"'

    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')

    # adding sheet
    ws = wb.add_sheet("sheet1")

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True

    # column header names, you can use your own headers here
    columns = ['Column 1', 'Column 2', 'Column 3', 'Column 4', ]

    # write column headers in sheet
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    dateFormte = datetime.datetime.strftime('%Y-%m-%d')

    # get your data, from database or from a text file...
    data = Income_Expense_LedgerValue1.objects.all()  # dummy method to fetch data.
    for my_row in data:
        row_num = row_num + 1
        ws.write(row_num, 0, my_row.dateOn.strftime('%d/%m/%Y'), font_style)
        ws.write(row_num, 1, my_row.type, font_style)
        ws.write(row_num, 2, my_row.amount, font_style)
        ws.write(row_num, 3, my_row.category_header, font_style)

    wb.save(response)
    return response


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=ledger' + str(datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['dateOn', 'type', 'amount', 'category_header', 'from_or_to_account', 'transaction_type',
                     'transaction_details', 'voucherNo_or_invoiceNo', 'remark', 'opening_balance_cash',
                     'closing_balance_cash',
                     'opening_balance_bank', 'closing_balance_bank',
                     'entry_time'])

    valuestore = Income_Expense_LedgerValue1.objects.filter(society_key=request.user.userpermission.society_key)

    for exp in valuestore:
        writer.writerow([exp.dateOn, exp.type, exp.amount, exp.category_header, exp.from_or_to_account,
                         exp.transaction_type,
                         exp.transaction_details, exp.voucherNo_or_invoiceNo, exp.remark, exp.opening_balance_cash,
                         exp.closing_balance_cash, exp.opening_balance_bank, exp.closing_balance_bank, exp.entry_time])

    return response


def demo(request, id):
    income_Expense_Ledger = Income_Expense_LedgerValue1.objects.get(id=id)

    if request.method == 'POST':
        text = request.POST['text']
        filestore = request.FILES['filestore']
        FileStoreValue1.objects.create(society_key=request.user.userpermission.society_key, text=text,
                                       type_file=filestore,
                                       income_Expense_LedgerId_id=income_Expense_Ledger.id)
        return redirect('demo', id)

    showfiles = FileStoreValue1.objects.filter(society_key=request.user.userpermission.society_key,
                                               income_Expense_LedgerId_id=income_Expense_Ledger)
    return render(request, 'demo.html', {'income_Expense_Ledger': income_Expense_Ledger, 'showfiles': showfiles})


def destroyFile(request, id):
    print("destroy showfiles -----------")
    showfiles = FileStoreValue1.objects.get(id=id)
    showfiles.delete()
    return redirect('/demo')


def showSubUser(request):
    print("allExpensiveCategory-----------")
    allsubUser = UserPermission.objects.filter(society_key=request.user.userpermission.society_key,
                                               is_society_admin=False, is_member=False)
    context = {
        'subUser': allsubUser
    }
    print(context)
    return render(request, 'showSubUser.html', context)


def addnewSubUser(request):
    if request.method == 'POST':
        contact_name = request.POST['contact_name']
        email = request.POST['email']
        password = make_password(request.POST['password'])
        phone_no = request.POST['phone_no']
        role = request.POST['Type']
        access_rights = request.POST['access_rights']
        status = request.POST['status']

        user_obj = User.objects.create(email=email, password=password, phone_no=phone_no, name=contact_name)

        sub_obj = UserPermission()
        sub_obj.user_key = user_obj
        sub_obj.society_key = request.user.userpermission.society_key
        sub_obj.role = role
        if access_rights == "Edit":
            sub_obj.is_edit = True
        if status == "Active":
            sub_obj.is_active = True
        sub_obj.save()
        return redirect('showSubUser')

    return render(request, 'addnewSubUser.html')


def editSubUser(request, id):
    subUser = UserPermission.objects.get(id=id)

    if request.method == 'POST':
        contact_name = request.POST['contact_name']
        email = request.POST['email']

        phone_no = request.POST['phone_no']
        Type = request.POST['Type']
        access_rights = request.POST['access_rights']
        status = request.POST['status']

        user_data = User.objects.get(pk=subUser.user_key.id)
        user_data.email = email
        user_data.phone_no = phone_no
        user_data.name = contact_name
        user_data.save()

        subUser.role = Type
        if access_rights == "Edit":
            subUser.is_edit = True
        if access_rights == "Read-Only":
            subUser.is_edit = False
        if status == "Active":
            subUser.is_active = True
        if status == "Inactive":
            subUser.is_active = False
        subUser.save()
        return redirect('showSubUser')

    return render(request, 'editSubUser.html', {'subUser': subUser})


def deleteSubUser(request, id):
    print("destroy Asset category-----------")
    subUser = UserPermission.objects.get(id=id).delete()
    return redirect("showSubUser")


def multi_deleteSubUser(request):
    print("Asset multi delete -------------")
    if request.method == "POST":
        product_ids = request.POST.getlist('id[]')
        print("delete this id ----------->", product_ids)
        for id in product_ids:
            subUser = UserPermission.objects.get(pk=id)
            subUser.delete()
            print(" subUser  delete this id ----------->", id)
        return redirect('showSubUser')


def all_deleteSubUser(request):
    print("subUser all delete -------------")
    if request.method == "POST":
        subUser = UserPermission.objects.filter(
            society_key=request.user.userpermission.society_key)
        subUser.delete()
        print(" subUser  delete this id ----------->")
        return redirect('showSubUser')


def AssetCategory(request):
    print("allAssetCategory-----------")
    allAssetCategory = AssentCategory1.objects.filter(society_key=request.user.userpermission.society_key)
    context = {
        'AssetCategory': allAssetCategory
    }
    print(context)
    return render(request, 'AssetCategory.html', context)


def addnewAssetCategory(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']

        AssentCategory1.objects.create(category_name=category_name, society_key=request.user.userpermission.society_key)
        return redirect('AssetCategory')
    return render(request, 'addAssetCategory.html')


def editAssetCategory(request, id):
    AssetCategory = AssentCategory1.objects.get(id=id)

    if request.method == 'POST':
        category_name = request.POST['category_name']
        AssetCategory.category_name = category_name
        AssetCategory.save()
        return redirect('AssetCategory')

    return render(request, 'editAssetCategory.html', {'AssetCategory': AssetCategory})


def deleteAssetCategory(request, id):
    print("destroy Asset category-----------")
    AssetCategory = AssentCategory1.objects.get(id=id).delete()
    return redirect("AssetCategory")


def multi_deleteAssetCategory(request):
    print("Asset multi delete -------------")
    if request.method == "POST":
        product_ids = request.POST.getlist('id[]')
        print("delete this id ----------->", product_ids)
        for id in product_ids:
            AssetCtaegory = AssentCategory1.objects.get(pk=id)
            AssetCtaegory.delete()
            print(" AssetCtaegory  delete this id ----------->", id)
        return redirect('AssetCategory')


def all_deleteAssetCategory(request):
    print("AssetCategory all delete -------------")
    if request.method == "POST":
        assetCategory = AssentCategory1.objects.filter(
            society_key=request.user.userpermission.society_key)
        assetCategory.delete()
        print(" AssetCategory  delete this id ----------->")
        return redirect('AssetCategory')


def export_users_xlsIassetCategory(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="assetCategory.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('assetCategory')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id', 'category_name']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = AssentCategory1.objects.filter(society_key=request.user.userpermission.society_key).values_list('id',
                                                                                                           'category_name')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def simple_uploadAssentCategory(request):
    if request.method == 'POST':
        emp_resource = AssentCategoryResource()
        dataset = Dataset()
        new_members = request.FILES['myfile']

        imported_data = dataset.load(new_members.read(), format='xlsx')
        for data in imported_data:
            AssentCategory1.objects.create(society_key=request.user.userpermission.society_key, category_name=data[0])

        return redirect('AssetCategory')


def Asset_InventoryCategory(request):
    print("allAsset_InventoryCategory-----------")
    allAsset_InventoryCategory = Asset_InventoryCategoryValue1.objects.filter(
        society_key=request.user.userpermission.society_key)
    context = {
        'assetinventorycategory': allAsset_InventoryCategory
    }
    print(context)
    return render(request, 'Asset_InventoryCategory.html', context)


def addnewAsset_InventoryCategory(request):
    allAsset = AssentCategory1.objects.filter(society_key=request.user.userpermission.society_key)
    context = {
        'allasset': allAsset
    }
    print(context)
    return render(request, 'addAsset_InventoryCategory.html', context)


def addNewRecordAssent_Inventory(request):
    itemName = request.POST['itemName']
    assetCategory = request.POST['assetCategory']
    quantity = request.POST['quantity']
    purchasePrice = request.POST['purchasePrice']
    deprecatedPrice = request.POST['deprecatedPrice']
    onDate = request.POST['onDate']

    totalCost = float(purchasePrice) * float(quantity)
    marketValue = float(deprecatedPrice) * float(quantity)

    Asset_InventoryCategoryValue1.objects.create(itemName=itemName, assetCategory=assetCategory, quantity=quantity,
                                                 purchasePrice=purchasePrice, deprecatedPrice=deprecatedPrice,
                                                 onDate=onDate,
                                                 totalCost=totalCost, marketValue=marketValue,
                                                 society_key=request.user.userpermission.society_key)
    return redirect('Asset_InventoryCategory')


def editAsset_InventoryCategory(request, id):
    assetinventorycategory = Asset_InventoryCategoryValue1.objects.get(id=id)

    if request.method == 'POST':
        itemName = request.POST['itemName']
        assetCategory = request.POST['assetCategory']
        quantity = request.POST['quantity']
        purchasePrice = request.POST['purchasePrice']
        deprecatedPrice = request.POST['deprecatedPrice']
        onDate = request.POST['onDate']

        assetinventorycategory.itemName = itemName
        assetinventorycategory.assetCategory = assetCategory
        assetinventorycategory.quantity = quantity
        assetinventorycategory.purchasePrice = purchasePrice
        assetinventorycategory.deprecatedPrice = deprecatedPrice
        assetinventorycategory.onDate = onDate
        assetinventorycategory.save()
        return redirect('Asset_InventoryCategory')

    return render(request, 'editAsset_InventoryCategory.html', {'assetinventorycategory': assetinventorycategory})


def destroyAsset_InventoryCategory(request, id):
    print("destroy Asset Inventory category-----------")
    assetinventorycategory = Asset_InventoryCategoryValue1.objects.get(id=id).delete()
    return redirect("Asset_InventoryCategory")


def multi_deleteAsset_InventoryCategory(request):
    print("Asset Inventory multi delete -------------")
    if request.method == "POST":
        product_ids = request.POST.getlist('id[]')
        print("delete this id ----------->", product_ids)
        for id in product_ids:
            assetinventorycategory = Asset_InventoryCategoryValue1.objects.get(pk=id)
            assetinventorycategory.delete()
            print(" Asset_InventoryCtaegory  delete this id ----------->", id)
        return redirect('Asset_InventoryCategory')


def all_deleteAsset_InventoryCategory(request):
    print("assetinventorycategory all delete -------------")
    if request.method == "POST":
        assetinventorycategory = Asset_InventoryCategoryValue1.objects.filter(
            society_key=request.user.userpermission.society_key)
        assetinventorycategory.delete()
        print(" assetinventorycategory  delete this id ----------->")
        return redirect('Asset_InventoryCategory')


def export_users_xlsIassetInventory(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="assetInventory.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('assetInventory')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id', 'itemName', 'assetCategory', 'quantity', 'purchasePrice', 'deprecatedPrice', 'onDate', 'totalCost',
               'marketValue']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Asset_InventoryCategoryValue1.objects.filter(
        society_key=request.user.userpermission.society_key).values_list('id', 'itemName',
                                                                         'assetCategory',
                                                                         'quantity',
                                                                         'purchasePrice',
                                                                         'deprecatedPrice',
                                                                         'onDate',
                                                                         'totalCost',
                                                                         'marketValue')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def simple_uploadAssentInventoryCategory(request):
    if request.method == 'POST':
        emp_resource = AssentInventoryResource()
        dataset = Dataset()
        new_members = request.FILES['myfile']

        imported_data = dataset.load(new_members.read(), format='xlsx')
        excelValue = []
        for data in imported_data:
            value = Asset_InventoryCategoryValue1.objects.create(society_key=request.user.userpermission.society_key,
                                                                 itemName=data[0],
                                                                 assetCategory=data[1],
                                                                 quantity=data[2], purchasePrice=data[3],
                                                                 deprecatedPrice=data[4],
                                                                 onDate=data[5])
            excelValue.append(value)

        for valueUpdate in excelValue:
            valueUpdate.totalCost = float(valueUpdate.purchasePrice) * float(valueUpdate.quantity)
            valueUpdate.marketValue = float(valueUpdate.deprecatedPrice) * float(valueUpdate.quantity)

            valueUpdate.save()

        return redirect('Asset_InventoryCategory')


def download_zipfile(request, id):
    from io import BytesIO
    import zipfile
    import os
    from django.conf import settings

    society_data = Society.objects.get(pk=id)

    all_file = FileStoreValue1.objects.filter(society_key=id)

    zip_file = []
    path = settings.MEDIA_ROOT

    for file in all_file:
        zip_file.append(file)

    filelist = zip_file
    byte_data = BytesIO()
    zip_name = "%s.zip" % society_data.society_name
    zip_file = zipfile.ZipFile(byte_data, 'w')

    for file in filelist:
        filename = os.path.basename(os.path.normpath(file.type_file.path))
        zip_file.write(file.type_file.path, filename)
    zip_file.close()

    response = HttpResponse(byte_data.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s' % zip_name

    zip_file.printdir()

    return response


def send_sms(request):
    import requests
    message_obj = MessageTemplate.objects.all().values()

    if request.method == 'POST':
        title = request.POST['template_name']
        number_type = request.POST['number']
        description = request.POST['description']

        print("---------------------------", description)

        memeber_data = MembersDeatilsValue.objects.filter(society_key=request.user.userpermission.society_key)
        message_data = MessageTemplate.objects.get(title__iexact=title)

        if number_type == 'secondaryContactNo':
            for number in memeber_data:
                if number.secondaryContactNo:
                    # dau = message_data.description.format()
                    final_sms_data = description.replace(' ', '%20')
                    url = AppData.objects.get(key__icontains="SMS_TEMPLATE_URL")
                    final_url = url.value.format(final_sms_data=final_sms_data, number=number.secondaryContactNo)
                    print(final_url)
                    requests.get(final_url)
                    return redirect('showMembersDetails')
                else:
                    return render(request, 'send_sms.html', {'message_obj': message_obj})
        if number_type == 'primaryContactNo':
            for number in memeber_data:
                if number.primaryContactNo:
                    final_sms_data = description.replace(' ', '%20')
                    url = AppData.objects.get(key__icontains="SMS_TEMPLATE_URL")
                    final_url = url.value.format(final_sms_data=final_sms_data, number=number.primaryContactNo)
                    print(final_url)
                    requests.get(final_url)
                    return redirect('showMembersDetails')
                else:
                    return render(request, 'send_sms.html', {'message_obj': message_obj})
        if number_type == 'whatsappContactNo':
            for number in memeber_data:
                if number.whatsappContactNo:
                    # dau = message_data.description.format()
                    final_sms_data = description.replace(' ', '%20')
                    url = AppData.objects.get(key__icontains="SMS_TEMPLATE_URL")
                    final_url = url.value.format(final_sms_data=final_sms_data, number=number.whatsappContactNo)
                    print(final_url)
                    requests.get(final_url)
                    return redirect('showMembersDetails')
                else:
                    return render(request, 'send_sms.html', {'message_obj': message_obj})
        all_number = []
        if number_type == 'allContactNo':
            for number in memeber_data:
                if number.whatsappContactNo:
                    if number.whatsappContactNo in all_number:
                        pass
                    else:
                        all_number.append(number.whatsappContactNo)
                if number.secondaryContactNo:
                    if number.secondaryContactNo in all_number:
                        pass
                    else:
                        all_number.append(number.secondaryContactNo)
                if number.primaryContactNo:
                    if number.primaryContactNo:
                        pass
                    else:
                        all_number.append(number.primaryContactNo)
                for number1 in all_number:
                    # dau = message_data.description.format()
                    final_sms_data = description.replace(' ', '%20')
                    url = AppData.objects.get(key__icontains="SMS_TEMPLATE_URL")
                    final_url = url.value.format(final_sms_data=final_sms_data, number=number1)
                    print(final_url)
                    requests.get(final_url)
                    return redirect('showMembersDetails')
        else:
            return render(request, 'send_sms.html', {'message_obj': message_obj})

    return render(request, 'send_sms.html', {'message_obj': message_obj})


def get_message(request):
    if request.method == 'GET':
        type_info = request.GET['type']

        data_dict = {}

        message_data = MessageTemplate.objects.filter(name__iexact = type_info)
        for message in message_data:
            data_dict['desc'] = message.desc

        if message_data:
            return JsonResponse(data_dict)

    return JsonResponse({'status':False})

