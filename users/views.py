from django.http import request
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from email.mime.text import MIMEText
import smtplib
from .forms import CustomUserCreationForm
from atom.settings import DEFAULT_FROM_EMAIL, EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_POST


# Create your views here.
def signup(request):
    if request.method == 'POST':
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
                PASSWORD = EMAIL_HOST_PASSWORD
                TO = input_email

                msg = MIMEText(
                    'Atomをご利用いただきありがとうございます。\n'
                    'あなたのアカウントは現在、仮登録の状態です。\n'
                    '以下のURLをクリックして、アカウントの本登録を行なってください。\n'
                    '\n'
                    'https://immense-falls-08135.herokuapp.com/signup/done/\n'
                    '\n'
                )
                msg['Subject'] = '【Atom】本登録をしてください'
                msg['From'] = DEFAULT_FROM_EMAIL
                msg['To'] = TO

                # access to the socket
                s = smtplib.SMTP(EMAIL_HOST, EMAIL_POST)
                s.starttls()
                s.login(EMAIL, PASSWORD)
                s.sendmail(EMAIL, TO, msg.as_string())
                s.quit()
                # スーバーユーザーが誤って退会してしまった時に再度ログインできるようにする
                if new_user.email == DEFAULT_FROM_EMAIL:
                    return render(request, 'users/pls_activate.html')
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
    return redirect('https://immense-falls-08135.herokuapp.com/admin/password_reset/')


@login_required
def index(request):
    return render(request, 'users/index.html')


@login_required
def select_house(request):
    # 要修正
    return render(request, 'users/index.html')


@login_required
def withdraw(request):
    user = request.user
    user.delete()
    return render(request, 'users/withdraw.html')


def policy(request):
    return render(request, 'users/policy.html')


def terms(request):
    return render(request, 'users/terms.html')
