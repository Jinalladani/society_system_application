from django.shortcuts import render
from myapp.models import User_Society_deatils

# Create your views here.
def dashbord(request):
    return render(request, 'myadminapp/dashbord.html')


def society_list(request):
    society_list = User_Society_deatils.objects.all()
    return render(request, 'myadminapp/society_list.html',{'society_list':society_list})
