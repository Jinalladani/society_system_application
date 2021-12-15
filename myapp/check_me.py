from django.shortcuts import redirect


def check_user(function):
    def wrapper(request, *args, **kwargs):
        user = request.User_Society_deatils
        if not user.is_authenticated:
            return redirect('loginpage')
        elif user.is_authenticated:
            return function(request, *args, **kwargs)

        return function(request, *args, **kwargs)

    return wrapper
