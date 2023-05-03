from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

from .utils import TokenGenerator, generate_token
from django.utils.encoding import force_str, force_bytes, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings


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
                messages.warning(request, "Email already in use!")
                return render(request, 'authentication/signup.html')

        except Exception as identifier:
            pass

        user = User.objects.create_user(email, email, password)
        user.is_active = False
        user.save()
        email_subject = "Activate your account!"
        message = render_to_string('authentication/activate.html',{
            'user': user,
            'domain': '127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })

        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER,
                                     [email])
        email_message.send()
        messages.success(request, "Activate your account by clicking link in your email")
        return render(request, "authentication/login.html")

    return render(request, "authentication/signup.html")


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if User is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.info(request, "Account Activated Successfully")
            return redirect("authentication/login.html")
        return render(request, "authentication/fail.html")


def handlelogin(request):
    if request.method == "POST":
        username = request.POST['email']
        userpassword = request.POST['pass1']
        myuser = authenticate(username=username, password=userpassword)
        if myuser is not None:
            login(request, myuser)
            return redirect('/')
        else:
            messages.warning(request, "Invalid Credentials")
            return redirect("/auth/login")

    return render(request, "authentication/login.html")


def handlelogout(request):
    logout(request)
    return redirect('/auth/login')


