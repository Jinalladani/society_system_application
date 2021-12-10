from django.shortcuts import render
from myapp.models import User_Society_deatils
from django.contrib.auth.models import User

# Create your views here.
def dashbord(request):
    return render(request, 'myadminapp/dashbord.html')


def society_list(request):
    society_list = User_Society_deatils.objects.all()
    return render(request, 'myadminapp/society_list.html',{'society_list':society_list})

def statusChange(request,id):
    statusChangeValue= User_Society_deatils.objects.get(id=id)
    print(statusChangeValue.is_active)
    if statusChangeValue.is_active == True:
        statusChangeValue = 'False'
    else:
        statusChangeValue = 'True'


def adminlogin(request):
    email = request.POST['email']
    password = request.POST['password']
