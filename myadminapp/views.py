from django.contrib import auth
from django.shortcuts import render, redirect
from myapp.models import Society
from accounts.models import User
from .forms import SocietyForm


# Create your views here.
def dashbord(request):
    NoOfSociety = Society.objects.count()
    print(NoOfSociety)

    activeSociety = Society.objects.filter(is_active=1).count()
    print(activeSociety)

    deactiveSociety = Society.objects.filter(is_active=0).count()
    print(deactiveSociety)

    # topData = society.objects.filter()

    return render(request, 'myadminapp/dashbord.html',{'NoOfSociety':NoOfSociety,'activeSociety':activeSociety,'deactiveSociety':deactiveSociety})


def society_list(request):
    if request.method == 'POST':
        contact_name = request.POST['contact_name']
        society_name = request.POST['society_name']
        city = request.POST['city']
        print(contact_name,society_name,city)

        society_list = Society.objects.all()

        if contact_name != "NULL":
            society_list = Society.objects.filter(contact_name=contact_name)
        if society_name != "NULL":
            society_list = Society.objects.filter(society_name=society_name)
        if city != "NULL":
            society_list = Society.objects.filter(city=city)
        print(society_list)
        return render(request, 'myadminapp/society_list.html', {'society_list': society_list})
    else:
        society_list = Society.objects.all()
        print("else")
        return render(request, 'myadminapp/society_list.html', {'society_list':society_list})


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
