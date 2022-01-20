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
from django.contrib import admin
from django.urls import path
from myadminapp import views
from myapp.check_me import check_user

urlpatterns = [
    path('',views.loginadminpage,name="loginadminpage"),
    path('dashbord',views.dashbord , name="dashbord"),
    path('adminlogin',views.adminlogin,name="adminlogin"),
    # path('logout', views.logout, name='logout'),
    path('society_list',views.society_list,name='society_list'),
    path('statusChange<int:id>',views.statusChange),
    path('editSocietyList/<int:id>', views.editSocietyList),
    path('destroySociety_list/<int:id>', views.destroySociety_list),
    path('appData_list',views.appData_list,name="appData_list"),
    path('editappData/<int:id>',views.editappData,name="editappData"),
    path('addNewaddData',views.addNewaddData,name="addNewaddData"),
]

