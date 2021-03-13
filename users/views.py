from django.http import request
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from email.mime.text import MIMEText
import smtplib
from .forms import CustomUserCreationForm
from atom.settings import DEFAULT_FROM_EMAIL


# Create your views here.
def signup(request):
    if request.method == 'POST':
        print("hoge")
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            input_email = form.cleaned_data['email']
            input_password = form.cleaned_data['password1']
            new_user = authenticate(email=input_email, password=input_password)
            if new_user is not None:
                login(request, new_user)

                # send mail for is_active false to true
                EMAIL = DEFAULT_FROM_EMAIL
                PASSWORD = 'gngemuzxfpkpegsa'
                TO = input_email

                msg = MIMEText(
                    'Hello.\n'
                    'Welcome to Djamazon.\n'
                    '\n'
                    'You created your own account on Djamazon.\n'
                    'From now on, you will get awesome experience!\n'
                    '\n'
                    'http://127.0.0.1:8000/signup/done/\n'
                    '\n'
                    'If you have a question, feel free to contact with us.\n'
                    '\n'
                    '\n'
                    'Sincerely,\n'
                    '\n'
                    '---------------------------------------------\n'
                    'Djamazon.Corporation\n'
                    '\n'
                    'Email: buru.aoshin@gmail.com\n'
                    '---------------------------------------------\n'
                )
                msg['Subject'] = '【Djamazon】Your account is created now'
                msg['From'] = DEFAULT_FROM_EMAIL
                msg['To'] = TO

                # access to the socket
                s = smtplib.SMTP(host='smtp.gmail.com', port=587)
                s.starttls()
                s.login(EMAIL, PASSWORD)
                s.sendmail(EMAIL, TO, msg.as_string())
                s.quit()
                new_user.is_active = False
                return render(request, 'users/pls_activate.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})


def pls_activate(request):
    return render(request, 'users/pls_activate.html')


def signup_done(request):
    user = request.user
    user.is_active = True
    user.save()
    login(request, user)
    return render(request, 'users/signup_done.html')


def password_reset(request):
    return redirect('http://127.0.0.1:8000/admin/password_reset/')


def index(request):
    return render(request, 'users/index.html')


def withdraw(request):
    user = request.user
    user.is_active = False
    user.save()
    return render(request, 'users/withdraw.html')
