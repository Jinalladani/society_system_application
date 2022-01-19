from django.contrib import auth
from django.shortcuts import render, redirect
from myapp.models import Society,AppData
from accounts.models import User


# Create your views here.
def dashbord(request):
    NoOfSociety = Society.objects.count()
    print(NoOfSociety)

    activeSociety = Society.objects.filter(is_active=True).count()
    print(activeSociety)

    deactiveSociety = Society.objects.filter(is_active=False).count()
    print(deactiveSociety)

    # topData = society.objects.filter()

    return render(request, 'myadminapp/dashbord.html',
                  {'NoOfSociety': NoOfSociety, 'activeSociety': activeSociety, 'deactiveSociety': deactiveSociety})


def society_list(request):
    if request.method == 'POST':
        contact_name = request.POST['contact_name']
        society_name = request.POST['society_name']
        city = request.POST['city']
        print(contact_name, society_name, city)

        society_list = Society.objects.all()

        if contact_name != "NULL":
            society_list = Society.filter(contact_name=contact_name)
        if society_name != "NULL":
            society_list = Society.filter(society_name=society_name)
        if city != "NULL":
            society_list = Society.filter(city=city)
        print(society_list)
        return render(request, 'myadminapp/society_list.html', {'society_list': society_list})
    else:
        society_list = Society.objects.all()
        print("else")
        return render(request, 'myadminapp/society_list.html', {'society_list': society_list})


def statusChange(request, id):
    User_Society_detail = Society.objects.get(id=id)
    if User_Society_detail:
        print('active')
        if User_Society_detail.is_active:
            User_Society_detail.is_active = False
            User_Society_detail.save()
            society_list = Society.objects.all()
            return render(request, 'myadminapp/society_list.html', {'society_list': society_list})
        else:
            User_Society_detail.is_active = True
            User_Society_detail.save()
            society_list = Society.objects.all()
            return render(request, 'myadminapp/society_list.html', {'society_list': society_list})
    else:
        society_list = Society.objects.all()
        return render(request, 'myadminapp/society_list.html', {'society_list': society_list})


def loginadminpage(request):
    return render(request, 'myadminapp/loginadmin.html')


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
                return redirect('dashbord')
        return render(request, 'myadminapp/loginadmin.html')


# def logout(request):
#     if request.method == 'POST':
#         auth.logout(request)
#     return redirect('loginadminpage')


def editSocietyList(request, id):
    print("edit ------------")
    society_list = Society.objects.get(id=id)
    return render(request, 'myadminapp/editSociety_list.html', {'society_list': society_list})


def updateSociety_list(request, id):
    print("update -------------")
    society_list = Society.objects.get(id=id)
    form = SocietyForm(request.POST, instance=society_list)
    if form.is_valid():
        form.save()
        return redirect("society_list")
    return render(request, 'myadminapp/editSociety_list.html', {'society_list': society_list})


def destroySociety_list(request, id):
    print("destroy category-----------")
    society_list = Society.objects.get(id=id)
    society_list.delete()
    return redirect("society_list")


def appData_list(request):
    appdata= AppData.objects.all()
    return render(request,'myadminapp/appData.html',{'appdata':appdata})


def addNewaddData(request):
    if request.method == "POST":
        key = request.POST['key']
        value = request.POST['value']

        AppData.objects.create(key=key,value=value)
        return redirect('appData_list')


    return render(request,'myadminapp/addNewaddData.html')


def editappData(request,id):
    appdata = AppData.objects.get(id=id)
    if request.method == "POST":
        key = request.POST['key']
        value = request.POST['value']
        appdata.key = key
        appdata.value = value
        appdata.save()
        return redirect('appData_list')

    return render(request,'myadminapp/editappData.html',{'appdata':appdata})