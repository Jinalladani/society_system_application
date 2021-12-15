from django.shortcuts import render, redirect
from myapp.models import User_Society_deatils
from django.contrib.auth.models import User

# Create your views here.
def dashbord(request):
    return render(request, 'myadminapp/dashbord.html')


def society_list(request):
    society_list = User_Society_deatils.objects.all()
    return render(request, 'myadminapp/society_list.html', {'society_list': society_list})


def statusChange(request, id):
    User_Society_detail = User_Society_deatils.objects.get(id=id)
    if User_Society_detail:
        print('active')
        if User_Society_detail.is_active:
            User_Society_detail.is_active = False
            User_Society_detail.save()
            return redirect('society_list')
        else:
            User_Society_detail.is_active = True
            User_Society_detail.save()
            society_list = User_Society_deatils.objects.all()
            return render(request, 'myadminapp/society_list.html', {'society_list': society_list})
    else:
        society_list = User_Society_deatils.objects.all()
        return render(request, 'myadminapp/society_list.html', {'society_list': society_list})

