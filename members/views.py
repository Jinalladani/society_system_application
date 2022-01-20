from django.shortcuts import render, redirect
from myapp.models import MembersDeatilsValue, UserPermission, Society, AppData
from accounts.models import User
from django.db.models import Q
from django.utils.crypto import get_random_string
import requests
from random import randint
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from .models import OtpSender
from userinterface.settings import Smsurl


# Create your views here.

def memberLoginPage(request):
    if request.method == 'POST':
        phone_no = request.POST['phone_no']
        member_data = MembersDeatilsValue.objects.filter(Q(primaryContactNo=phone_no)
                                                         | Q(whatsappContactNo=phone_no)
                                                         | Q(secondaryContactNo=phone_no))

        if member_data:
            random_otp = randint(000000, 999999)

            url_path = AppData.objects.filter(key__icontains = "SMSURL")
            if url_path:
                url = url_path.get(key__icontains="SMSURL")
                final_url = url.value.format(phone_no=phone_no, otp=random_otp)
            else:
                url = Smsurl
                final_url = url.format(phone_no=phone_no, otp=random_otp)


            requests.get(final_url)

            OtpSender.objects.create(number=phone_no, otp_data=random_otp)
            return redirect('send_otpMoblie', phone_no)

    message="Number does not exist"
    return render(request, 'memberLogin.html',{'message':message})


def send_otpMoblie(request, number, *args, **kwargs):
    if request.method == 'POST':
        otp = request.POST['otp']

        confirm_data = OtpSender.objects.filter(number__iexact=number).last()

        if int(confirm_data.otp_data) == int(otp):
            member_data = MembersDeatilsValue.objects.filter(Q(primaryContactNo=number)
                                                             | Q(whatsappContactNo=number)
                                                             | Q(secondaryContactNo=number))
            if member_data.count() > 1:
                context = {
                    'member_data': member_data,
                    'phone_no': number,
                }

                return render(request, 'multiSociety.html', context)

            user_data = User.objects.filter(phone_no=number)

            print(user_data)

            if user_data is not None:
                user_data = User.objects.filter(phone_no=number)
                user_data.update(password=make_password(otp))
                user = user_data.get(phone_no=number)

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
            else:
                email_data = ""
                for member in member_data:
                    password = make_password(otp)
                    user_obj = User.objects.create(email=member.email, password=password, phone_no=number)

                    email_data = member.email

                    sub_obj = UserPermission()
                    sub_obj.user_key = user_obj
                    society_instance = Society.objects.get(pk=member.society_key.id)
                    sub_obj.society_key = society_instance
                    sub_obj.is_active = True
                    sub_obj.is_member = True
                    sub_obj.save()

                user = auth.authenticate(email=email_data, password=number)

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

        else:
            print(number)
            print("not same")

    return render(request, 'send-otpMoblie.html', {'phone_no': number})


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
