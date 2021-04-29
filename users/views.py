from django.http import request
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from axes.backends import AxesBackend
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
from .models import Inquire
from .forms import CustomUserCreationForm, HouseChooseForm, TwoStepAuthForm
from . import utils
from users.models import User, Inquire
from atom.settings import DEBUG, DEFAULT_FROM_EMAIL, EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_POST


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            input_email = form.cleaned_data['email']
            input_password = form.cleaned_data['password1']
            new_user = authenticate(
                request=request, email=input_email, password=input_password)
            if new_user is not None:
                login(request, new_user)
                EMAIL = DEFAULT_FROM_EMAIL
                PASSWORD = EMAIL_HOST_PASSWORD
                TO = input_email
                msg = MIMEMultipart('alternative')
                msg['Subject'] = '【Atom】本登録をしてください / Please make a formal registration'
                msg['From'] = DEFAULT_FROM_EMAIL
                msg['To'] = TO
                if DEBUG:
                    html = """\
                    <head>
                      <link rel="preconnect" href="https://fonts.gstatic.com">
　　　　　　            <link href="https://fonts.googleapis.com/css2?family=Krona+One&display=swap" rel="stylesheet">
                      <link href="https://fonts.googleapis.com/css2?family=Monoton&display=swap" rel="stylesheet">
                      <style type="text/css">
                        p, a {font-size:10.0pt; font-family:'Krona One', sans-serif; color:#383636;}
                      </style>
                    </head>
                    <body>
                      <p style="font-size:20.0pt; font-family:'Monoton', cursive;">Hi! We are the ATOM's mail system.</p>
                      <br><br>
                      <p>Atomをご利用いただきありがとうございます。</p>
                      <p>あなたのアカウントは現在、仮登録の状態です。</p>
                      <p>以下のURLをクリックして、アカウントの本登録を行なってください。</p>
                      <br>
                      <a href="http://127.0.0.1:8000/signup/doing/">http://127.0.0.1:8000/signup/doing/</a>
                      <br><br>
                      <p>Thank you for using Atom. </p>
                      <p>Your account is currently in a temporary registration status.</p>
                      <p>Click the URL below to register your account</p>
                      <br>
                      <a href="http://127.0.0.1:8000/signup/doing/">http://127.0.0.1:8000/signup/doing/</a>
                      <br>
                      <p>Thank you.</p>
                      <hr>
                      <img style="padding:5px 5px 0px 0px; float:left; width:20px;" src="cid:{logo_image}" alt="Logo">
                      <p style="color:#609bb6;">From Atom team</p>
                      </div>
                    </body>
                    </html>
                    """
                else:
                    html = """\
                    <head>
                      <link rel="preconnect" href="https://fonts.gstatic.com">
　　　　　　            <link href="https://fonts.googleapis.com/css2?family=Krona+One&display=swap" rel="stylesheet">
                      <link href="https://fonts.googleapis.com/css2?family=Monoton&display=swap" rel="stylesheet">
                      <style type="text/css">
                        p, a {font-size:10.0pt; font-family:'Krona One', sans-serif; color:#383636;}
                      </style>
                    </head>
                    <body>
                      <p style="font-size:20.0pt; font-family:'Monoton', cursive;">Hi! We are the ATOM's mail system.</p>
                      <br><br>
                      <p>Atomをご利用いただきありがとうございます。</p>
                      <p>あなたのアカウントは現在、仮登録の状態です。</p>
                      <p>以下のURLをクリックして、アカウントの本登録を行なってください。</p>
                      <br>
                      <a href="https://atom-production.herokuapp.com/signup/doing/">https://atom-production.herokuapp.com/signup/doing/</a>
                      <br><br>
                      <p>Thank you for using Atom. </p>
                      <p>Your account is currently in a temporary registration status.</p>
                      <p>Click the URL below to register your account</p>
                      <br>
                      <a href="https://atom-production.herokuapp.com/signup/doing/">https://atom-production.herokuapp.com/signup/doing/</a>
                      <br>
                      <p>Thank you.</p>
                      <hr>
                      <img style="padding:5px 5px 0px 0px; float:left; width:20px;" src="cid:{logo_image}" alt="Logo">
                      <p style="color:#609bb6;">From Atom team</p>
                      </div>
                    </body>
                    </html>
                    """
                fp = open('static/img/users/icon.png', 'rb')
                img = MIMEImage(fp.read())
                fp.close()
                img.add_header('Content-ID', '<logo_image>')
                msg.attach(img)
                template = MIMEText(html, 'html')
                msg.attach(template)
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


def pls_activate(request):
    return render(request, 'users/pls_activate.html')


def signup_doing(request):
    user = User.objects.get(id=request.user.id)
    request.session["img"] = utils.get_image_b64(
        utils.get_auth_url(user.email, utils.get_secret(user)))
    two_step_auth_form = TwoStepAuthForm()
    return render(request, 'users/signup_doing.html', {'two_step_auth_form': two_step_auth_form})


def signup_done(request):
    user = User.objects.get(id=request.user.id)
    user.is_active = True
    user.save()
    return render(request, 'users/signup_done.html')


def password_reset(request):
    if DEBUG:
        return redirect('http://127.0.0.1:8000/admin/password_reset/')
    else:
        return redirect('https://atom-production.herokuapp.com/admin/password_reset/')


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
def request_ch_house(request):
    user = User.objects.get(id=request.user.id)
    EMAIL = user.email
    PASSWORD = EMAIL_HOST_PASSWORD
    TO = DEFAULT_FROM_EMAIL
    msg = MIMEMultipart('alternative')
    msg['Subject'] = '【Atom】ユーザーからハウス変更の申請が届きました'
    msg['From'] = EMAIL
    msg['To'] = TO
    html = """\
    <html>
    <head>
      <link rel="preconnect" href="https://fonts.gstatic.com">
　　　 <link href="https://fonts.googleapis.com/css2?family=Krona+One&display=swap" rel="stylesheet">
      <link href="https://fonts.googleapis.com/css2?family=Monoton&display=swap" rel="stylesheet">
      <style type="text/css">
        p, a {font-size:10.0pt; font-family:'Krona One', sans-serif; color:#383636;}
      </style>
    </head>
    <body>
      <p style="font-size:20.0pt; font-family:'Monoton', cursive;">Hi! We are the ATOM's mail system.</p>
      <br><br>
      <p>ユーザーからハウス変更の申請が届きました。</p>
      <a href="https://atom-production.herokuapp.com/admin/">管理画面へ</a>
      <br>
      <p>Thank you.</p>
      <hr>
      <img style="padding:5px 5px 0px 0px; float:left; width:20px;" src="cid:{logo_image}" alt="Logo">
      <p style="color:#609bb6;">From Atom team</p>
      </div>
    </body>
    </html>
    """
    fp = open('static/img/users/icon.png', 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    img.add_header('Content-ID', '<logo_image>')
    msg.attach(img)
    template = MIMEText(html, 'html')
    msg.attach(template)
    s = smtplib.SMTP(EMAIL_HOST, EMAIL_POST)
    s.starttls()
    s.login(DEFAULT_FROM_EMAIL, PASSWORD)
    s.sendmail(EMAIL, TO, msg.as_string())
    s.quit()
    messages.success(
        request, f"ハウス名変更の申請が完了しました。 / The application for changing the house name has been completed.")
    return render(request, 'users/index.html')


@login_required
def request_house_owner(request):
    user = User.objects.get(id=request.user.id)
    EMAIL = user.email
    PASSWORD = EMAIL_HOST_PASSWORD
    TO = DEFAULT_FROM_EMAIL
    msg = MIMEMultipart('alternative')
    msg['Subject'] = '【Atom】ユーザーからハウス管理者権限の申請が届きました'
    msg['From'] = EMAIL
    msg['To'] = TO
    html = """\
    <html>
    <head>
      <link rel="preconnect" href="https://fonts.gstatic.com">
　　　 <link href="https://fonts.googleapis.com/css2?family=Krona+One&display=swap" rel="stylesheet">
      <link href="https://fonts.googleapis.com/css2?family=Monoton&display=swap" rel="stylesheet">
      <style type="text/css">
        p, a {font-size:10.0pt; font-family:'Krona One', sans-serif; color:#383636;}
      </style>
    </head>
    <body>
      <p style="font-size:20.0pt; font-family:'Monoton', cursive;">Hi! We are the ATOM's mail system.</p>
      <br><br>
      <p>ユーザーからハウス管理者権限の申請が届きました。</p>
      <p>’is_staff’をTrueにしてください。</p>
      <a href="https://atom-production.herokuapp.com/admin/">管理画面へ</a>
      <br>
      <p>Thank you.</p>
      <br><br><br>
      <hr>
      <img style="padding:5px 5px 0px 0px; float:left; width:20px;" src="cid:{logo_image}" alt="Logo">
      <p style="color:#609bb6;">From Atom team</p>
      </div>
    </body>
    </html>
      """
    fp = open('static/img/users/icon.png', 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    img.add_header('Content-ID', '<logo_image>')
    msg.attach(img)
    template = MIMEText(html, 'html')
    msg.attach(template)
    s = smtplib.SMTP(EMAIL_HOST, EMAIL_POST)
    s.starttls()
    s.login(DEFAULT_FROM_EMAIL, PASSWORD)
    s.sendmail(EMAIL, TO, msg.as_string())
    s.quit()
    messages.success(
        request, f"ハウス管理者権限の申請が完了しました。 / Application for house administrator authority has been completed.")
    return render(request, 'users/index.html')


def inquire(request):
    content = request.GET.get(key='content')
    inquire = Inquire(content=content,)
    inquire.save()
    user = User.objects.get(id=request.user.id)
    EMAIL = user.email
    PASSWORD = EMAIL_HOST_PASSWORD
    TO = DEFAULT_FROM_EMAIL
    msg = MIMEMultipart('alternative')
    msg['Subject'] = '【Atom】ユーザーから問い合わせを受けました'
    msg['From'] = EMAIL
    msg['To'] = TO
    html = """\
    <html>
    <head>
      <link rel="preconnect" href="https://fonts.gstatic.com">
　　　 <link href="https://fonts.googleapis.com/css2?family=Krona+One&display=swap" rel="stylesheet">
      <link href="https://fonts.googleapis.com/css2?family=Monoton&display=swap" rel="stylesheet">
      <style type="text/css">
        p, a {font-size:10.0pt; font-family:'Krona One', sans-serif; color:#383636;}
      </style>
    </head>
    <body>
      <p style="font-size:20.0pt; font-family:'Monoton', cursive;">Hi! We are the ATOM's mail system.</p>
      <br><br>
      <p>ユーザーから問い合わせが受けました。</p>
      <a href="https://atom-production.herokuapp.com/admin/">管理画面へ</a>
      <br>
      <p>Thank you.</p>
      <hr>
      <img style="padding:5px 5px 0px 0px; float:left; width:20px;" src="cid:{logo_image}" alt="Logo">
      <p style="color:#609bb6;">From Atom team</p>
      </div>
    </body>
    </html>
    """

    fp = open('static/img/users/icon.png', 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    img.add_header('Content-ID', '<logo_image>')
    msg.attach(img)
    template = MIMEText(html, 'html')
    msg.attach(template)
    s = smtplib.SMTP(EMAIL_HOST, EMAIL_POST)
    s.starttls()
    s.login(DEFAULT_FROM_EMAIL, PASSWORD)
    s.sendmail(EMAIL, TO, msg.as_string())
    s.quit()
    messages.success(
        request, f"サポートセンターに問い合わせを送信しました。 / You have sent an inquiry to the support center.")
    return redirect('users:login')


@login_required
def withdraw(request):
    user = User.objects.get(id=request.user.id)
    user.is_active = False
    return render(request, 'users/withdraw.html')


def policy(request):
    return render(request, 'users/policy.html')


def terms(request):
    return render(request, 'users/terms.html')


def axes_locked(request):
    return render(request, 'users/axes_locked.html')
