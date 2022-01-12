from django.urls import path
from members import views

urlpatterns = [
    path('',views.memberLoginPage,name="memberlogin"),
    path('send_otpMoblie',views.send_otpMoblie,name="send_otpMoblie"),
    # path('', views.memberLoginPage, name='memberlogin')
]