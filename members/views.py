from django.shortcuts import render, redirect
from myapp.models import MembersDeatilsValue, UserPermission, Society
from accounts.models import User
from django.db.models import Q
from django.utils.crypto import get_random_string
import requests
from random import randint
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from .models import OtpSender
# Create your views here.

def memberLoginPage(request):
    if request.method == 'POST':
        phone_no = request.POST['phone_no']
        member_data = MembersDeatilsValue.objects.filter(Q(primaryContactNo=phone_no)
                                                         | Q(whatsappContactNo=phone_no)
                                                         | Q(secondaryContactNo=phone_no))

        if member_data:
            random_otp = randint(000000, 999999)
            requests.get("http://quicksms.highspeedsms.com/sendsms/sendsms.php?username=BREbonrix&password=sales55&type=TEXT&sender=BONRIX&mobile="+str(phone_no)+"&message=Your%20OTP%20for%20login%20verification%20is%20:=%20"+str(random_otp)+"")

            OtpSender.objects.create(number=phone_no, otp_data=random_otp)
            return redirect('send_otpMoblie', phone_no)

    return render(request, 'memberLogin.html')


def send_otpMoblie(request, phone_no, *args, **kwargs):

    # if request.method == 'POST':
    #     otp = request.POST['otp']
    #     generate_otp = request.POST['generateotp']
    #     phone_no = request.POST['phone_no']
    #
    #     if otp == generate_otp:
    #         member_data = MembersDeatilsValue.objects.filter(Q(primaryContactNo=phone_no)
    #                                                          | Q(whatsappContactNo=phone_no)
    #                                                          | Q(secondaryContactNo=phone_no))
    #         if member_data.count() > 1 :
    #
    #             context = {
    #                 'member_data':member_data,
    #                 'phone_no':phone_no,
    #             }
    #
    #             return render(request, 'multiSociety.html', context)
    #
    #         if User.objects.filter(phone_no = phone_no):
    #            user_data = User.objects.filter(phone_no = phone_no)
    #            user_data.update(password = make_password(phone_no))
    #            user = user_data.get(phone_no = phone_no)
    #
    #            user_permission = UserPermission.objects.get(user_key=user)
    #            if user_permission:
    #                if user_permission.is_active:
    #                    auth.login(request, user)
    #                    return redirect('index')
    #                else:
    #                    return redirect('loginpage')
    #            else:
    #                if user:
    #                    auth.login(request, user)
    #                    return redirect('index')
    #                else:
    #                    return redirect('loginpage')
    #         else:
    #             email_data = ""
    #             for member in member_data:
    #                 password = make_password(phone_no)
    #                 user_obj = User.objects.create(email=member.email, password=password, phone_no=phone_no)
    #
    #                 email_data = member.email
    #
    #                 sub_obj = UserPermission()
    #                 sub_obj.user_key = user_obj
    #                 society_instance = Society.objects.get(pk = member.society_key.id)
    #                 sub_obj.society_key = society_instance
    #                 sub_obj.is_active = True
    #                 sub_obj.is_member = True
    #                 sub_obj.save()
    #
    #             user = auth.authenticate(email=email_data, password=phone_no)
    #
    #             user_permission = UserPermission.objects.get(user_key=user)
    #
    #             if user_permission:
    #                 if user_permission.is_active:
    #                     auth.login(request, user)
    #                     return redirect('index')
    #                 else:
    #                     return redirect('loginpage')
    #             else:
    #                 if user:
    #                     auth.login(request, user)
    #                     return redirect('index')
    #                 else:
    #                     return redirect('loginpage')
    #
    #     else:
    #         print(phone_no)
    #         print("not same")

    return render(request, 'send-otpMoblie.html')


def MultiSociety(request):

    if request.method == 'POST':
        society_key = request.POST['society']
        phone_no = request.POST['phone_no']
        member_data = request.POST['member_data']

        if User.objects.filter(phone_no=phone_no):
            user_data = User.objects.filter(phone_no=phone_no)
            user_data.update(password=make_password(phone_no))
            user = user_data.get(phone_no=phone_no)

            society_instance = Society.objects.get(pk=society_key)

            user_permission = UserPermission.objects.get(user_key=user)
            user_permission.society_key = society_instance
            user_permission.save()
            if user_permission:
                if user_permission.is_active:
                    auth.login(request, user)
                    return redirect('index')
                else:
                    return redirect('loginpage')
            else:
                if user:
                    auth.login(request, user)
                    return redirect('index')
                else:
                    return redirect('loginpage')
        else:
            email_data = ""
            for member in member_data:
                password = make_password(phone_no)
                user_obj = User.objects.create(email=member.email, password=password, phone_no=phone_no)

                email_data = member.email

                sub_obj = UserPermission()
                sub_obj.user_key = user_obj
                society_instance = Society.objects.get(pk=society_key)
                sub_obj.society_key = society_instance
                sub_obj.is_active = True
                sub_obj.is_member = True
                sub_obj.save()

            user = auth.authenticate(email=email_data, password=phone_no)

            user_permission = UserPermission.objects.get(user_key=user)

            if user_permission:
                if user_permission.is_active:
                    auth.login(request, user)
                    return redirect('index')
                else:
                    return redirect('loginpage')
            else:
                if user:
                    auth.login(request, user)
                    return redirect('index')
                else:
                    return redirect('loginpage')

    return render(request, 'multiSociety.html')