from django.shortcuts import render
from myapp.models import MembersDeatilsValue
from django.db.models import Q


# Create your views here.

def memberLoginPage(request):
    if request.method == 'POST':
        phone_no = request.POST['phone_no']
        member_data = MembersDeatilsValue.objects.filter(Q(primaryContactNo=phone_no)
                                                         | Q(whatsappContactNo=phone_no)
                                                         | Q(secondaryContactNo=phone_no))

        for member in member_data:
            print(member.email)
            print("----------")
        if member_data:
            return render(request, 'send-otpMoblie.html',{'phone_no':phone_no})

    return render(request, 'memberLogin.html')


def send_otpMoblie(request):
    # otp = user password
    # if password phone email alogin
    return render(request, 'send-otpMoblie.html')
