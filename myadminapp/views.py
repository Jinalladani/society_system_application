from django.contrib import auth
from django.shortcuts import render, redirect
from myapp.models import Society,AppData , UserPermission, FileStoreValue1
from accounts.models import User


# Create your views here.
def admindashbord(request):
    NoOfSociety = Society.objects.count()
    print(NoOfSociety)

    activeSociety = Society.objects.filter(is_active=True).count()
    print(activeSociety)

    deactiveSociety = Society.objects.filter(is_active=False).count()
    print(deactiveSociety)

    # topData = society.objects.filter()

    return render(request, 'admindashbord.html',
                  {'NoOfSociety': NoOfSociety, 'activeSociety': activeSociety, 'deactiveSociety': deactiveSociety})


def society_list1(request):
    if request.method == 'POST':
        contact_name = request.POST['contact_name']
        society_name = request.POST['society_name']
        email = request.POST['city']

        society_list = Society.objects.all()
        if contact_name:
            society_list = Society.objects.filter(contact_name__startswith=contact_name)
        if society_name:
            society_list = Society.objects.filter(society_name__startswith=society_name)
        if email:
            society_list = Society.objects.filter(email__startswith=email)
        return render(request, 'society_list.html', {'society_list': society_list})

    society_list = Society.objects.all()
    return render(request, 'society_list.html', {'society_list': society_list})


def viewSocietyProfile(request,id):
    socDeatils = Society.objects.get(id=id)
    return render(request, 'viewSocietyProfile.html',{'socDeatils':socDeatils})


def statusChange(request, id):
    User_Society_detail = Society.objects.get(id=id)
    if User_Society_detail:
        print('active')
        if User_Society_detail.is_active:
            User_Society_detail.is_active = False
            User_Society_detail.save()
            society_list = Society.objects.all()
            return render(request, 'society_list.html', {'society_list': society_list})
        else:
            User_Society_detail.is_active = True
            User_Society_detail.save()
            society_list = Society.objects.all()
            return render(request, 'society_list.html', {'society_list': society_list})
    else:
        society_list = Society.objects.all()
        return render(request, 'society_list.html', {'society_list': society_list})


def loginadminpage(request):
    return render(request, 'loginadmin.html')


def adminlogin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user.is_staff:
            print(user)
            if user:
                print("stafff-------------")
                auth.login(request, user)
                return redirect('admindashbord')
        return render(request, 'loginadmin.html')


def editSocietyList(request, id):
    society_list = Society.objects.get(id=id)

    if request.method == 'POST':
        email = request.POST['email']
        phone_no = request.POST['phone_no']
        contact_name = request.POST['contact_name']
        society_name = request.POST['society_name']
        society_address = request.POST['society_address']
        city = request.POST['city']
        pin_code = request.POST['pin_code']
        state = request.POST['state']
        country = request.POST['country']
        society_registration_number = request.POST['society_registration_number']

        society_list.email = email
        society_list.phone_no = phone_no
        society_list.contact_name = contact_name
        society_list.society_name = society_name
        society_list.society_address = society_address
        society_list.city = city
        society_list.pin_code = pin_code
        society_list.state = state
        society_list.country = country
        society_list.society_registration_number = society_registration_number
        society_list.save()
        return redirect("society_list")

    return render(request, 'editSociety_list.html', {'society_list': society_list})



def destroySociety_list(request):

    id = request.POST['id']
    print(id)
    print("===========")
    society_list = Society.objects.get(id=id)

    user_data = UserPermission.objects.filter(society_key = society_list.id)

    file_obj = FileStoreValue1.objects.filter(society_key = society_list).delete()

    total_user = []
    for user in user_data:
        total_user.append(user.user_key.id)

    user_io = User.objects.filter(pk__in = total_user).delete()
    society_list.delete()


    return redirect("society_list")



def appData_list(request):
    appdata= AppData.objects.all()
    return render(request,'appData.html',{'appdata':appdata})


def addNewaddData(request):
    if request.method == "POST":
        key = request.POST['key']
        value = request.POST['value']

        AppData.objects.create(key=key,value=value)
        return redirect('appData_list')


    return render(request,'addNewaddData.html')


def editappData(request,id):
    appdata = AppData.objects.get(id=id)
    if request.method == "POST":
        key = request.POST['key']
        value = request.POST['value']
        appdata.key = key
        appdata.value = value
        appdata.save()
        return redirect('appData_list')

    return render(request,'editappData.html',{'appdata':appdata})

