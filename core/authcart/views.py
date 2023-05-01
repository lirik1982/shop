from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User

def signup(request):
    if request.method == "POST":
        email=request.POST['email']
        password=request.POST['pass1']
        password_confirm=request.POST['pass2']
        if password != password_confirm:
            messages.warning(request, 'Passwords is not match!')
            return render(request, 'authentication/signup.html')

        try:
            if User.objects.get(username=email):
                return HttpResponse('Email already in use')
        except Exception as identifier:
            pass

        user = User.objects.create_user(email, email, password)
        user.save()
        return HttpResponse("User Created", email)

    return render(request, "authentication/signup.html")


def handlelogin(request):
    return render(request, "authentication/login.html")


def handlelogout(request):
    return redirect('/auth/login')


