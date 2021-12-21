import csv
from django.contrib import auth
from django.db.models import Sum
from tablib import Dataset
from .models import SocietyDeatils, ExpenseCategory, IncomeCategory, Income_Expense_LedgerValue1, \
    BalanceValue, \
    Members_Vendor_Account, FileStoreValue1, MembersDeatilsValue, AssentCategory, Society
from .forms import ExpensiveCategoryForm, IncomeCategoryForm, BalanceFrom, \
    Members_Vendor_AccountForm, MembersDeatilsForm
from .resource import ExpenseResource, IncomeResource, Members_VendoorsResource, Income_Expense_LedgerResource, \
    MembersDetailsResource
from django.shortcuts import render, redirect
import xlwt
from django.http import HttpResponse
import datetime
from .check_me import check_user
from accounts.models import User
from django.contrib.auth.hashers import make_password


def index(request):
    balance = BalanceValue.objects.filter(society_key=request.user.society)

    contentBalance = {
        'balanceValue': balance
    }
    print(contentBalance)

    totalExpense = Income_Expense_LedgerValue1.objects.filter(society_key=request.user.society,
                                                              type='Expense').aggregate(Sum('amount'))
    print(totalExpense)

    totalIncome = Income_Expense_LedgerValue1.objects.filter(society_key=request.user.society,
                                                             type='Income').aggregate(
        Sum('amount'))
    print(totalIncome)

    listExpense = ExpenseCategory.objects.filter(society_key=request.user.society)
    print(listExpense)

    expenseAmountSum = Income_Expense_LedgerValue1.objects.values('category_header').filter(
        society_key=request.user.society, type='Expense').annotate(
        totalamount=Sum('amount'))
    print(expenseAmountSum)

    listIncome = IncomeCategory.objects.filter(society_key=request.user.society)
    print(listIncome)

    incomeAmountSum = Income_Expense_LedgerValue1.objects.values('category_header').filter(
        society_key=request.user.society, type='Income').annotate(
        totalamount=Sum('amount'))
    print(incomeAmountSum)

    topExpense = Income_Expense_LedgerValue1.objects.values('from_or_to_account', 'category_header',
                                                            'transaction_type', 'amount').filter(
        society_key=request.user.society, type='Expense').order_by('amount').reverse()[0:20]
    print("---------topExpense-------------", topExpense)

    topIncome = Income_Expense_LedgerValue1.objects.values('from_or_to_account', 'category_header',
                                                           'transaction_type', 'amount').filter(
        society_key=request.user.society, type='Income').order_by('amount').reverse()[0:20]
    print(topIncome)

    topMemberExpense = Income_Expense_LedgerValue1.objects.values('from_or_to_account').annotate(
        amount=Sum('amount')).filter(society_key=request.user.society, type='Expense').order_by(
        'amount').reverse()[
                       0:20]

    topMemberIncome = Income_Expense_LedgerValue1.objects.values('from_or_to_account').annotate(
        amount=Sum('amount')).filter(society_key=request.user.society, type='Income').order_by(
        'amount').reverse()[0:20]

    return render(request, 'index.html',
                  {'contentBalance': contentBalance, 'totalExpense': totalExpense, 'totalIncome': totalIncome,
                   'listExpense': listExpense, 'listIncome': listIncome, 'expenseAmountSum': expenseAmountSum,
                   'incomeAmountSum': incomeAmountSum, 'topExpense': topExpense, 'topIncome': topIncome,
                   'topMemberExpense': topMemberExpense, 'topMemberIncome': topMemberIncome
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
    # societyDeatils = Society.objects.filter(society_key=request.user.society)
    societyDeatils = Society.objects.all()
    return render(request, 'societyProfile.html',{'societyDeatils':societyDeatils})


# def multi_delete(request):
#     print("post delete -------------")
#     if request.method == "POST":
#         product_ids = request.POST.getlist('id[]')
#         print("delete this id ----------->", product_ids)
#         for id in product_ids:
#             employee = Employee.objects.get(pk=id)
#             employee.delete()
#             print(" employe  delete this id ----------->", id)
#         return redirect('show')


def login(request):
    email = request.POST['email']
    password = request.POST['password']

    user = auth.authenticate(email=email, password=password)
    print(user)
    if user:
        auth.login(request, user)
        return redirect('index')
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

        user_instance = User.objects.get(pk=uid.id)

        Society.objects.create(user_key=user_instance, email=email, phone_no=phone_no, contact_name=contact_name,
                               society_name=society_name,
                               society_address=society_address,
                               city=city, pin_code=pin_code, state=state, country=country,
                               society_registration_number=society_registration_number)
        return redirect('loginpage')

    return render(request, 'login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect('loginpage')


def ExpensiveCategory(request):
    print("allExpensiveCategory-----------")
    allExpensiveCategory = ExpenseCategory.objects.filter(society_key=request.user.society)
    context = {
        'expensiveCategory': allExpensiveCategory
    }
    print(context)
    return render(request, 'ExpensiveCategory.html', context)


def addnewExpensiveCategory(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']

        ExpenseCategory.objects.create(category_name=category_name, society_key=request.user.society)
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


# def AssentCategory(request):
#     allAssentCategory = AssentCategory.objects.all()
#     context = {
#         'assentCategory': allAssentCategory
#     }
#     return render(request, 'AssentCategory.html', context)


def IncomeCategoryshow(request):
    print("allIncomeCategory-----------")
    allIncomeCategory = IncomeCategory.objects.filter(society_key=request.user.society)
    context = {
        'incomeCategory': allIncomeCategory
    }
    print(context)
    return render(request, 'incomeCategory.html', context)


def addnewIncomeCategory(request):
    print("add new Income Category--------------------")
    if request.method == 'POST':
        category_name = request.POST['category_name']

        IncomeCategory.objects.create(category_name=category_name, society_key=request.user.society)
        return redirect('IncomeCategory')

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
        return redirect('IncomeCategory')


def multipleSearch(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        ledgerobj = Income_Expense_LedgerValue1.objects.raw(
            'select * from myapp_income_expense_ledgervalue1 where type ="' + type + '"')
        return render(request, 'showIncome_expense_ledger.html', {'ledgerobj': ledgerobj})
    else:
        allincome_expense_ledger = Income_Expense_LedgerValue1.objects.all()
        return redirect('showIncome_expense_ledger')


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
        allmembersValue = Members_Vendor_Account.objects.filter(society_key=request.user.society)
        contextMember = {
            'memberValue': allmembersValue
        }
        print(contextMember)

        if to_date == "":
            to_date = dateOn
        income_expense_ledger = Income_Expense_LedgerValue1.objects.filter(society_key=request.user.society)

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
        allincome_expense_ledger = Income_Expense_LedgerValue1.objects.filter(society_key=request.user.society)
        context = {
            'income_expense_ledger': allincome_expense_ledger
        }
        print(context)
        print("else")
        return render(request, 'showIncome_expense_ledger.html', context)


def addincome_expense_ledger(request):
    print("add  Income_expense_ledger Category--------------------")
    allexpValue = ExpenseCategory.objects.filter(society_key=request.user.society)
    context = {
        'expValue': allexpValue
    }
    print(context)
    allincValue = IncomeCategory.objects.filter(society_key=request.user.society)
    contextIncome = {
        'incValue': allincValue
    }
    print(contextIncome)
    allmembersValue = Members_Vendor_Account.objects.filter(society_key=request.user.society)
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
    balance_set = BalanceValue.objects.filter(society_key=request.user.society,account='Cash')
    print("balance ------------>", balance_set)
    for balance in balance_set:
        bal_amount = float(balance.balance_amount)
    print('bal_amount------', bal_amount)
    obc = bal_amount
    cbc = obc

    balance_set = BalanceValue.objects.filter(society_key=request.user.society,account='Bank')
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

    entry_time = datetime.datetime.now()

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
                                                     society_key=request.user.society)
    print(uid)
    updateBalanceValue(cbc, cbb)
    return redirect('showincome_expense_ledger')


def updateBalanceValue(cbc, cbb):
    caseObject = BalanceValue.objects.get(account='Cash')
    print("cbc -------------", cbc)
    print(caseObject)
    caseObject.balance_amount = cbc
    caseObject.save()
    bankObject = BalanceValue.objects.get(account='Bank')
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
    entry_time = datetime.datetime.now()

    amount1 = float(amount)
    balance_set = BalanceValue.objects.filter(society_key=request.user.society,account='Cash')
    print("balance ------------>", balance_set)
    for balance in balance_set:
        bal_amount = float(balance.balance_amount)
    print('bal_amount------', bal_amount)
    obc = bal_amount
    cbc = obc

    balance_set = BalanceValue.objects.filter(society_key=request.user.society,account='Bank')
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
                                                                   society_key=request.user.society)
    updateBalanceValue(cbc, cbb)
    balance_set = BalanceValue.objects.filter(society_key=request.user.society,account='Bank')
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
                                                                   society_key=request.user.society)
    updateBalanceValue(cbc, cbb)
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
    entry_time = datetime.datetime.now()

    amount1 = float(amount)
    balance_set = BalanceValue.objects.filter(society_key=request.user.society,account='Cash')
    print("balance ------------>", balance_set)
    bal_amount = 0
    for balance in balance_set:
        bal_amount = float(balance.balance_amount)
    print('bal_amount------', bal_amount)
    obc = bal_amount
    cbc = obc

    balance_set = BalanceValue.objects.filter(society_key=request.user.society,account='Bank')
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
                                                                   society_key=request.user.society)
    updateBalanceValue(cbc, cbb)
    balance_set = BalanceValue.objects.filter(society_key=request.user.society,account='Cash')
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
                                                                   society_key=request.user.society)
    updateBalanceValue(cbc, cbb)
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


# def updateIncome_expense_ledger(request, id):
#     if request.POST:
#         dateOn = request.POST['date']
#         type = request.POST['type']
#         amount = request.POST['amount']
#         category_header = request.POST['category_header']
#         from_or_to_account = request.POST['from_or_to_account']
#         transaction_type = request.POST['transaction_type']
#         transaction_details = request.POST['transaction_details']
#         voucherNo_or_invoiceNo = request.POST['voucherNo_or_invoiceNo']
#         remark = request.POST['remark']
#         income_expense_ledger = Income_Expense_LedgerValue1.objects.get(id=id)
#         income_expense_ledger.dateOn = dateOn
#         income_expense_ledger.type = type
#         income_expense_ledger.amount = amount
#         income_expense_ledger.category_header = category_header
#         income_expense_ledger.from_or_to_account = from_or_to_account
#         income_expense_ledger.transaction_type = transaction_type
#         income_expense_ledger.transaction_details = transaction_details
#         income_expense_ledger.voucherNo_or_invoiceNo = voucherNo_or_invoiceNo
#         income_expense_ledger.remark = remark
#         income_expense_ledger.save()
#         return redirect('showincome_expense_ledger')
#     else:
#         # print("update Income_expense_ledger-------------")
#         income_expense_ledger = Income_Expense_LedgerValue1.objects.get(id=id)
#         print('income_expense_ledger', income_expense_ledger)
#         form = Income_Expense_LedgerForm(request.POST, instance=income_expense_ledger)
#         return render(request, 'editIncome_expense_ledger.html', {'income_expense_ledger': income_expense_ledger})


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
        return redirect('show')


def showBalance(request):
    print("all Balance-----------")
    allBalance = BalanceValue.objects.filter(society_key=request.user.society)
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
        BalanceValue.objects.create(account=account, balance_amount=balance_amount,
                                    society_key=request.user.society)
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
    allMembers_vendor = Members_Vendor_Account.objects.filter(society_key=request.user.society)
    context = {
        'members_vendor': allMembers_vendor
    }
    print(context)
    return render(request, 'showMembers_vendor.html', context)


def addnewMembers_vendor(request):
    print("add new Members_vendor--------------------")
    if request.method == 'POST':
        name = request.POST['name']
        Members_Vendor_Account.objects.create(name=name, society_key=request.user.society)
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


def showMembersDetails(request):
    print("show MembersDetails-----------")
    allMembersDetails = MembersDeatilsValue.objects.filter(society_key=request.user.society)
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
                                           society_key=request.user.society)
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

    rows = ExpenseCategory.objects.filter(society_key=request.user.society).values_list('id', 'category_name')
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

    rows = IncomeCategory.objects.filter(society_key=request.user.society).values_list('id', 'category_name')
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

    rows = Members_Vendor_Account.objects.filter(society_key=request.user.society).values_list('id', 'name')
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

    rows = MembersDeatilsValue.objects.filter(society_key=request.user.society).values_list('id', 'flatNo',
                                                                                            'primaryName',
                                                                                            'primaryContactNo',
                                                                                            'secondaryName',
                                                                                            'secondaryContactNo',
                                                                                            'accountingName',
                                                                                            'whatsappContactNo',
                                                                                            'email', 'residence')
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

    rows = Income_Expense_LedgerValue1.objects.filter(society_key=request.user.society).values_list('id', 'dateOn',
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
            print(data[0])
            value = ExpenseCategory(
                data[0],
                data[1]
            )
            value.save()
        return redirect('ExpensiveCategory')


def simple_uploadIncome(request):
    if request.method == 'POST':
        emp_resource = ExpenseResource()
        dataset = Dataset()
        new_expense = request.FILES['myfile']

        imported_data = dataset.load(new_expense.read(), format='xlsx')
        # print(imported_data)
        for data in imported_data:
            print(data[1])
            value = ExpenseCategory(
                data[0],
                data[1]
            )
            value.save()

    return redirect('ExpensiveCategory')


# def simple_uploadIncome(request):
#     if request.method == 'POST':
#         emp_resource = IncomeResource()
#         dataset = Dataset()
#         new_income = request.FILES['myfile']
#
#         imported_data = dataset.load(new_income.read(), format='xlsx')
#         # print(imported_data)
#         for data in imported_data:
#             print(data[0])
#             value = IncomeCategory(
#                 data[0],
#                 data[1]
#             )
#             value.save()
#
#     return redirect('IncomeCategoryshow')


def simple_uploadMembers_Vendors(request):
    if request.method == 'POST':
        emp_resource = Members_VendoorsResource()
        dataset = Dataset()
        new_members = request.FILES['myfile']

        imported_data = dataset.load(new_members.read(), format='xlsx')
        # print(imported_data)
        for data in imported_data:
            print(data[1])
            value = Members_Vendor_Account(
                data[0],
                data[1]
            )
            value.save()

    return redirect('showMembers_Vendor')


def simple_uploadMembersDetails(request):
    if request.method == 'POST':
        emp_resource = MembersDetailsResource()
        dataset = Dataset()
        new_members = request.FILES['myfile']

        imported_data = dataset.load(new_members.read(), format='xlsx')
        # print(imported_data)
        for data in imported_data:
            print(data[1])
            value = MembersDeatilsValue(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                data[8]
            )
            value.save()

    return redirect('showMembersDetails')


def simple_uploadIncome_Expense_Ledger(request):
    if request.method == 'POST':
        emp_resource = Income_Expense_LedgerResource()
        dataset = Dataset()
        new_income = request.FILES['myfile']

        imported_data = dataset.load(new_income.read(), format='xlsx')
        # print(imported_data)
        excelValue = []
        for data in imported_data:
            print(data[1])
            value = Income_Expense_LedgerValue1(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                data[8],
                data[9],
                0,
                0,
                0,
                0
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

            balance_set = BalanceValue.objects.all().filter(account='Cash')
            for balance in balance_set:
                bal_amount = float(balance.balance_amount)

            valueUpdate.opening_balance_cash = bal_amount
            valueUpdate.closing_balance_cash = valueUpdate.opening_balance_cash

            balance_set = BalanceValue.objects.all().filter(account='Bank')
            for balance in balance_set:
                bal_amountBank = float(balance.balance_amount)
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

            valueUpdate.entry_time = datetime.datetime.now()

            if Members_Vendor_Account.objects.all().filter(name=valueUpdate.from_or_to_account):
                print("record found")
            else:
                print("record not found")
                checkmember = Members_Vendor_Account.objects.create(name=valueUpdate.from_or_to_account)

            if valueUpdate.type == 'Expense':
                if ExpenseCategory.objects.all().filter(category_name=valueUpdate.category_header):
                    print("record found")
                else:
                    print("record not found")
                    checkexpense = ExpenseCategory.objects.create(category_name=valueUpdate.category_header)

            if valueUpdate.type == 'Income':
                if IncomeCategory.objects.all().filter(category_name=valueUpdate.category_header):
                    print("record found")
                else:
                    print("record not found")
                    checkexpense = IncomeCategory.objects.create(category_name=valueUpdate.category_header)

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
                                         , valueUpdate.closing_balance_bank)
        # value.save()

    return redirect('showincome_expense_ledger')


def updateBalanceValueUploadFile(cbc, cbb):
    caseObject = BalanceValue.objects.get(account='Cash')
    print("cbc -------------", cbc)
    print(caseObject)
    caseObject.balance_amount = cbc
    caseObject.save()
    bankObject = BalanceValue.objects.get(account='Bank')
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
    response['Content-Disposition'] = 'attachment; filename=ledger' + str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['id', 'dateOn', 'type', 'amount', 'category_header', 'from_or_to_account', 'transaction_type',
                     'transaction_details', 'voucherNo_or_invoiceNo', 'remark', 'opening_balance_cash',
                     'closing_balance_cash',
                     'opening_balance_bank', 'closing_balance_bank',
                     'entry_time'])

    valuestore = Income_Expense_LedgerValue1.objects.all()

    for exp in valuestore:
        writer.writerow([exp.id, exp.dateOn, exp.type, exp.amount, exp.category_header, exp.from_or_to_account,
                         exp.transaction_type,
                         exp.transaction_details, exp.voucherNo_or_invoiceNo, exp.remark, exp.opening_balance_cash,
                         exp.closing_balance_cash, exp.opening_balance_bank, exp.closing_balance_bank, exp.entry_time])

    return response


# def file_store(request):
#     income_Expense_LedgerId = request.POST['income_Expense_LedgerId']
#     text = request.POST['text']
#     filestore = request.FILES['filestore']
#     print("--------------", text, income_Expense_LedgerId, filestore)
#     fileid = FileStoreValue1.objects.create(text=text, type_file=filestore,
#                                             income_Expense_LedgerId_id=income_Expense_LedgerId)
#     showfiles = FileStoreValue1.objects.filter(income_Expense_LedgerId_id=income_Expense_LedgerId)
#     # return redirect('/showincome_expense_ledger')
#     return render(request, 'demo.html', {'showfiles': showfiles})
#
#
# def demo(request, id):
#     income_Expense_Ledger = Income_Expense_LedgerValue1.objects.get(id=id)
#     showfiles = FileStoreValue1.objects.filter(income_Expense_LedgerId_id=income_Expense_Ledger)
#     return render(request, 'demo.html', {'income_Expense_Ledger': income_Expense_Ledger, 'showfiles': showfiles})
#
#
# def destroyFile(request, id):
#     print("destroy showfiles -----------")
#     showfiles = FileStoreValue1.objects.get(id=id)
#     showfiles.delete()
#     return redirect('/demo')

def demo(request, id):
    income_Expense_Ledger = Income_Expense_LedgerValue1.objects.get(id=id)

    if request.method == 'POST':
        text = request.POST['text']
        filestore = request.FILES['filestore']
        FileStoreValue1.objects.create(society_key=request.user.society, text=text, type_file=filestore,
                                       income_Expense_LedgerId_id=income_Expense_Ledger.id)
        return redirect('demo', id)

    showfiles = FileStoreValue1.objects.filter(society_key=request.user.society,
                                               income_Expense_LedgerId_id=income_Expense_Ledger)
    return render(request, 'demo.html', {'income_Expense_Ledger': income_Expense_Ledger, 'showfiles': showfiles})


def destroyFile(request, id):
    print("destroy showfiles -----------")
    showfiles = FileStoreValue1.objects.get(id=id)
    showfiles.delete()
    return redirect('/demo')
