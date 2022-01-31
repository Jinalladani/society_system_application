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
from .check_me import  check_user, login_user

urlpatterns = [
    path('',login_user(views.loginadminpage),name="loginadminpage"),
    path('admindashbord', views.admindashbord , name="admindashbord"),
    path('adminlogin',login_user(views.adminlogin),name="adminlogin"),
    # path('logout', views.logout, name='logout'),
    path('society_list1',check_user(views.society_list1),name='society_list1'),
    path('statusChange<int:id>',views.statusChange),
    path('editSocietyList/<int:id>', views.editSocietyList),
    path('destroySociety_list/', views.destroySociety_list, name='removesociety'),
    path('appData_list',check_user(views.appData_list),name="appData_list"),
    path('editappData/<int:id>',views.editappData,name="editappData"),
    path('addNewaddData',views.addNewaddData,name="addNewaddData"),
    path('viewSocietyProfile/<int:id>',views.viewSocietyProfile,name="viewSocietyProfile"),
    path('sms_templatesList',views.sms_templatesList,name="sms_templatesList"),
    path('addsms_templates',views.addsms_templates,name="addsms_templates"),
    path('editsms_templates/<int:id>',views.editsms_templates,name="editsms_templates"),
    path('deletesms_templates/<int:id>',views.deletesms_templates,name="deletesms_templates"),
]

