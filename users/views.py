from django.http import request
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from email.mime.text import MIMEText
import smtplib
from .forms import CustomUserCreationForm, HouseChooseForm
from atom.settings import DEBUG, DEFAULT_FROM_EMAIL, EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_POST


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
                EMAIL = DEFAULT_FROM_EMAIL
                PASSWORD = EMAIL_HOST_PASSWORD
                TO = input_email
                if DEBUG:
                    msg = MIMEText(
                        'Atomをご利用いただきありがとうございます。\n'
                        'あなたのアカウントは現在、仮登録の状態です。\n'
                        '以下のURLをクリックして、アカウントの本登録を行なってください。\n'
                        '\n'
                        'http://127.0.0.1:8000/signup/done/\n'
                        '\n'
                        '\n'
                        '\n'
                        'Thank you for using Atom. \n'
                        'Your account is currently in a temporary registration status. \n'
                        'Click the URL below to register your account. \n'
                        '\n'
                        'http://127.0.0.1:8000/signup/done/\n'
                        '\n'
                    )
                else:
                    msg = MIMEText(
                        'Atomをご利用いただきありがとうございます。\n'
                        'あなたのアカウントは現在、仮登録の状態です。\n'
                        '以下のURLをクリックして、アカウントの本登録を行なってください。\n'
                        '\n'
                        'https://glacial-shore-75579.herokuapp.com/signup/done/\n'
                        '\n'
                        '\n'
                        '\n'
                        'Thank you for using Atom. \n'
                        'Your account is currently in a temporary registration status. \n'
                        'Click the URL below to register your account. \n'
                        '\n'
                        'https://glacial-shore-75579.herokuapp.com/signup/done/\n'
                        '\n'
                    )
                msg['Subject'] = '【Atom】本登録をしてください / Please make a formal registration'
                msg['From'] = DEFAULT_FROM_EMAIL
                msg['To'] = TO
                s = smtplib.SMTP(EMAIL_HOST, EMAIL_POST)
                s.starttls()
                s.login(EMAIL, PASSWORD)
                s.sendmail(EMAIL, TO, msg.as_string())
                s.quit()
                if new_user.email == DEFAULT_FROM_EMAIL:
                    return render(request, 'users/pls_activate.html')
                else:
                    new_user.is_active = False
                return render(request, 'users/pls_activate.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})


def signup_done(request):
    user = request.user
    user.is_active = True
    user.save()
    return render(request, 'users/signup_done.html')


def password_reset(request):
    if DEBUG:
        return redirect('http://127.0.0.1:8000/admin/password_reset/')
    else:
        return redirect('https://glacial-shore-75579.herokuapp.com/admin/password_reset/')


@login_required
def index(request):
    house_choose_form = HouseChooseForm(request.POST or None)
    if house_choose_form.is_valid():
        name = house_choose_form.cleaned_data['name']
        user = request.user
        user.house = name
        user.save()
        return render(request, 'app/room.html')
    ctx = {
        'house_choose_form': house_choose_form,
    }
    return render(request, 'users/index.html', ctx)


@login_required
def withdraw(request):
    user = request.user
    user.delete()
    return render(request, 'users/withdraw.html')


def policy(request):
    return render(request, 'users/policy.html')


def terms(request):
    return render(request, 'users/terms.html')
