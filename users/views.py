import smtplib
from django.http import request
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from axes.backends import AxesBackend
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from .models import User, Inquire, RequestHouseOwner
from .forms import CustomUserCreationForm, HouseChooseForm, TwoStepAuthForm
from . import utils
from app.models import HouseChore
from app.forms import AddHousechoreForm
from atom.settings import DEBUG, DEFAULT_FROM_EMAIL, EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_POST


# Create your views here.
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

                # send mail for is_active false to true
                try:
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

                    # access to the socket
                    s = smtplib.SMTP(EMAIL_HOST, EMAIL_POST)
                    s.starttls()
                    s.login(EMAIL, PASSWORD)
                    s.sendmail(EMAIL, TO, msg.as_string())
                    s.quit()
                    # スーバーユーザーが誤って退会してしまった時に再度ログインできるようにする
                    if new_user.email == DEFAULT_FROM_EMAIL:
                        return render(request, 'users/pls_activate.html')
                    else:
                        new_user.is_active = False
                    return render(request, 'users/pls_activate.html')

                except:
                    messages.warning(
                        request, f"メール送信に失敗しました。しばらくしてもう一度お試しください。/ Failed to send the email. Please try again after a while."
                    )

    else:
        form = CustomUserCreationForm()
    return render(request, 'users/auth/signup.html', {'form': form})


def pls_activate(request):
    return render(request, 'users/auth/pls_activate.html')


# 2 step google authenticate
def signup_doing(request):
    # user = request.user
    user = User.objects.get(id=request.user.id)
    # QRコード生成
    request.session["img"] = utils.get_image_b64(
        utils.get_auth_url(user.email, utils.get_secret(user)))
    two_step_auth_form = TwoStepAuthForm()
    return render(request, 'users/auth/signup_doing.html', {'two_step_auth_form': two_step_auth_form})


def signup_done(request):
    user = User.objects.get(id=request.user.id)
    user.is_active = True
    user.save()
    return render(request, 'users/auth/signup_done.html')


def password_reset(request):
    if DEBUG:
        return redirect('http://127.0.0.1:8000/admin/password_reset/')
    else:
        return redirect('https://atom-production.herokuapp.com/admin/password_reset/')


@login_required
def index(request):
    # ハウス名を選択させるためのリストを作成する
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
@require_POST
def request_house_owner(request):
    user = request.user
    RequestHouseOwner(email=user.email, house=user.house).save()

    try:
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
          <a href="https://atom-production.herokuapp.com/manage_top/">管理画面へ</a>
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

        # access to the socket
        s = smtplib.SMTP(EMAIL_HOST, EMAIL_POST)
        s.starttls()
        s.login(DEFAULT_FROM_EMAIL, PASSWORD)
        s.sendmail(EMAIL, TO, msg.as_string())
        s.quit()
        messages.success(
            request, f"ハウス管理者権限の申請が完了しました。 / Application for house administrator authority has been completed.")

    except:
        messages.warning(
            request, f"メール送信に失敗しました。しばらくしてもう一度お試しください。/ Failed to send the email. Please try again after a while."
        )

    return redirect('users:index')


def inquire(request):
    content = request.GET.get(key='content')
    inquire = Inquire(content=content,)
    inquire.save()

    try:
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
          <a href="https://atom-production.herokuapp.com/manage_top/">管理画面へ</a>
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
        # Define the image's ID as referenced above
        img.add_header('Content-ID', '<logo_image>')
        msg.attach(img)

        template = MIMEText(html, 'html')
        msg.attach(template)

        # access to the socket
        s = smtplib.SMTP(EMAIL_HOST, EMAIL_POST)
        s.starttls()
        s.login(DEFAULT_FROM_EMAIL, PASSWORD)
        s.sendmail(EMAIL, TO, msg.as_string())
        s.quit()
        messages.success(
            request, f"サポートセンターに問い合わせを送信しました。 / You have sent an inquiry to the support center.")
    except:
        messages.warning(
            request, f"メール送信に失敗しました。しばらくしてもう一度お試しください。/ Failed to send the email. Please try again after a while."
        )

    return redirect('users:login')


@login_required
def withdraw(request):
    user = User.objects.get(id=request.user.id)[0]
    user.is_active = False
    user.save()
    return render(request, 'users/auth/withdraw.html')


def policy(request):
    return render(request, 'users/policy.html')


def terms(request):
    return render(request, 'users/terms.html')


def axes_locked(request):
    return render(request, 'users/auth/axes_locked.html')


def manage_top(request):
    return render(request, 'users/manage/manage_top.html')


@login_required
@staff_member_required
def manage(request):
    form = AddHousechoreForm(request.POST or None)
    housemates = User.objects.filter(
        house=request.user.house, is_active=True).order_by('id')
    housechores = HouseChore.objects.filter(
        house=request.user.house).order_by('id')
    ctx = {
        'housemates': housemates,
        'housechores': housechores,
        'form': form,
    }
    return render(request, 'users/manage/manage.html', ctx)


@login_required
@staff_member_required
def housemate_detail(request, housemate_id):
    housemate = get_object_or_404(User, pk=housemate_id)
    ctx = {
        'housemate': housemate,
    }
    return render(request, 'users/manage/housemate_detail.html', ctx)


@login_required
@staff_member_required
def housechore_detail(request, housechore_id):
    housechore = get_object_or_404(HouseChore, pk=housechore_id)
    ctx = {
        'housechore': housechore,
    }
    return render(request, 'users/manage/housechore_detail.html', ctx)


@login_required
@staff_member_required
@require_POST
def add_housechore(request):
    user = request.user
    title = request.POST.get('title')
    description = request.POST.get('description')
    HouseChore(title=title, description=description, house=user.house).save()
    return redirect('users:manage')


@login_required
@staff_member_required
@require_POST
def update_housechore(request):
    id = request.POST.get('id')
    title = request.POST.get('title')
    description = request.POST.get('description')
    housechore = HouseChore.objects.filter(id=id)[0]
    housechore.title = title
    housechore.description = description
    housechore.save()
    messages.success(
        request, f"{title}を更新しました。/ {title} has been updated.")
    return redirect('users:manage')


@login_required
@staff_member_required
@require_POST
def delete_housechore(request):
    try:
        title = request.POST.get('housechore_title')
        housechore = HouseChore.objects.filter(title=title)[0]
        housechore.delete()
        messages.success(
            request, f"{title}を削除しました。/ {title} has been deleted.")
    except:
        messages.warning(
            request, f"家事がありません。/ There are no housechore."
        )
    return redirect('users:manage')


@login_required
@staff_member_required
@require_POST
def deactivate_housemate(request):
    email = request.POST.get('housemate_email')
    user = User.objects.filter(email=email)[0]
    user.is_active = False
    user.save()
    messages.success(
        request, f"{email}をdeactivateしました。/ {email} has been deactivated.")
    return redirect('users:manage')
