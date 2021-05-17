import smtplib
from django.http import request
from django.http.response import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.views.decorators.http import require_POST
from django.template import Context, Template
from axes.backends import AxesBackend
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from email.mime.image import MIMEImage
from .models import User, Inquire, RequestHouseOwner
from .forms import CustomUserCreationForm, HouseChooseForm
from app.models import HouseChore
from app.forms import AddHousechoreForm
from atom.settings import DEBUG, DEFAULT_FROM_EMAIL, EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_POST


# Create your views here.
# https://www.sejuku.net/blog/31661
# def session_control(request):
#     if request.session.get(request, False):
#         messages.warning(
#             request, f"複数回連続では実行できません。/ You cannot execute multiple times in a row.")
#     request.session[request] = True


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

                # アクティベーションURLの送付
                current_site = get_current_site(request)
                domain = current_site.domain

                # send mail for is_active false to true
                EMAIL = DEFAULT_FROM_EMAIL
                PASSWORD = EMAIL_HOST_PASSWORD
                TO = input_email

                msg = MIMEMultipart('alternative')
                msg['Subject'] = '【Atom】本登録をしてください / Please make a formal registration'
                msg['From'] = DEFAULT_FROM_EMAIL
                msg['To'] = TO

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
                    <p>{{ TO }} 様</p>
                    <p>Atomをご利用いただきありがとうございます。</p>
                    <p>あなたのアカウント（{{ TO }}）は現在、仮登録の状態です。</p>
                    <p>1時間以内に以下のURLをクリックして、アカウントの本登録を行なってください。</p>
                    <br>
                    <p>{{ protocol }}://{{ domain }}{% url 'users:signup_doing' token %}</p>
                    <br><br>
                    <p>Thank you for using Atom. </p>
                    <p>Your account（{{ TO }}）is currently in a temporary registration status.</p>
                    <p>Click the URL below to register your account within 1 hour.</p>
                    <br>
                    <p>{{ protocol }}://{{ domain }}{% url 'users:signup_doing' token %}</p>
                    <br>
                    <p>Thank you.</p>
                </body>
                </html>
                """

                # fp = open('static/img/users/icon.png', 'rb')
                # img = MIMEImage(fp.read())
                # fp.close()
                # # Define the image's ID as referenced above
                # img.add_header('Content-ID', '<logo_image>')
                # msg.attach(img)
                html = Template(html)
                context = Context({
                    'TO': TO,
                    'protocol': request.scheme,
                    'domain': domain,
                    'token': dumps(new_user.pk),
                })
                template = MIMEText(html.render(context=context), 'html')
                msg.attach(template)

                try:
                    # access to the socket
                    s = smtplib.SMTP(EMAIL_HOST, EMAIL_POST)
                    s.starttls()
                    s.login(EMAIL, PASSWORD)
                    s.sendmail(EMAIL, TO, msg.as_string())
                    s.quit()
                except Exception:
                    messages.warning(
                        request, f"メール送信に失敗しました。しばらくしてもう一度お試しください。/ Failed to send the email. Please try again after a while."
                    )

                # スーバーユーザー(自分)は最初からis_active=Trueにしておく。
                if new_user.email != DEFAULT_FROM_EMAIL:
                    new_user.is_active = False
                    new_user.save()
                ctx = {
                    'new_user': new_user
                }
                return render(request, 'users/auth/pls_activate.html', ctx)

    else:
        form = CustomUserCreationForm()
    return render(request, 'users/auth/signup.html', {'form': form})


def pls_activate(request):
    return render(request, 'users/auth/pls_activate.html')


def signup_doing(request, **kwargs):
    token = kwargs.get('token')
    return render(request, 'users/auth/signup_doing.html', {'token': token})


def signup_done(request):
    # デフォルトでは1日以内なので、1時間に設定
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*1)
    # tokenが正しければ本登録
    token = request.GET.get('token')
    try:
        # user_pk = loads(token)
        user_pk = loads(token, max_age=timeout_seconds)
    # 期限切れ
    except SignatureExpired:
        return HttpResponseBadRequest()
    # tokenが間違っている
    except BadSignature:
        return HttpResponseBadRequest()

    # tokenは問題なし
    else:
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return HttpResponseBadRequest()
        else:
            if not user.is_active:
                user.is_active = True
                user.save()
                return render(request, 'users/auth/signup_done.html')

    return HttpResponseBadRequest()


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

        # ハウス管理者に、自分のハウスに新規家事割り当て対象ユーザーが追加された旨の通知メールを送る
        if user.is_staff == False:
            user_id = user.id
            EMAIL = user.email
            PASSWORD = EMAIL_HOST_PASSWORD
            TO = User.objects.filter(house=request.user.house, is_active='True',
                                     is_staff='True').values_list('email')[0][0]

            msg = MIMEMultipart('alternative')
            msg['Subject'] = '【Atom】あなたのハウスにユーザーが新規登録しました'
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
            <p>ユーザー（ユーザーID：{{ user_id }}）（メールアドレス：{{ EMAIL }}）があなたのハウスに新規登録しました。</p>
            <p>A user (user ID: {{user_id}}) (email address: {{EMAIL}}) has newly registered in your house.</p>
            <p>次回の家事割り振りの対象になります。</p>
            <p>He/she will be the target of the next housechore allocation.</p>
            <p>心当たりがない場合は、管理画面からユーザーをdeactivateしてください。</p>
            <p>If you have no idea, deactivate the user from the below admin page.</p>
            <a href="https://atom-production.herokuapp.com/manage_top/">管理画面へ|Go to admin page</a>
            <br>
            <p>Thank you.</p>
            </body>
            </html>
            """

        html = Template(html)
        context = Context({'user_id': user_id, 'EMAIL': EMAIL})
        template = MIMEText(html.render(context=context), 'html')
        msg.attach(template)

        try:
            # access to the socket
            s = smtplib.SMTP(EMAIL_HOST, EMAIL_POST)
            s.starttls()
            s.login(DEFAULT_FROM_EMAIL, PASSWORD)
            s.sendmail(EMAIL, TO, msg.as_string())
            s.quit()
            messages.success(
                request, f"ハウス管理者に、あなたが新規登録した事を報告しました。/ Reported to the house manager that you have newly registered.")
            return redirect("app:room")
        except:
            messages.warning(
                request, f"ハウス管理者に、あなたが新規登録した事を報告できませんでした。直接お伝えください。/ Could not report to the house manager that you have newly registered. Please tell him/her directly.")
            return redirect("app:room")

    ctx = {
        'house_choose_form': house_choose_form,
    }

    return render(request, 'users/index.html', ctx)


@login_required
@require_POST
def request_house_owner(request):
    # 連続投稿を防ぐ
    session_control()

    user = request.user
    user_id = user.id
    RequestHouseOwner(email=user.email, house=user.house).save()

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
      <p>ユーザー（ユーザーID：{{ user_id }}）（メールアドレス：{{ EMAIL }}）からハウス管理者権限の申請が届きました。</p>
      <p>’is_staff’をTrueにしてください。</p>
      <a href="https://atom-production.herokuapp.com/manage_top/">管理画面へ</a>
      <br>
      <p>Thank you.</p>
    </body>
    </html>
    """

    html = Template(html)
    context = Context({'user_id': user_id, 'EMAIL': EMAIL})
    template = MIMEText(html.render(context=context), 'html')
    msg.attach(template)

    try:
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


@login_required
def inquire(request):
    content = request.GET.get(key='content')
    inquire = Inquire(content=content,)
    inquire.save()

    user = User.objects.get(id=request.user.id)
    user_id = user.id
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
      <p>ユーザー（ユーザーID：{{ user_id }}）（メールアドレス：{{ EMAIL }}）から問い合わせが受けました。</p>
      <hr>
      <p>問い合わせ内容</p>
      <p>{{ content }}</p>
      <hr>
      <a href="https://atom-production.herokuapp.com/manage_top/">管理画面へ</a>
      <br>
      <p>Thank you.</p>
    </body>
    </html>
    """

    html = Template(html)
    context = Context(
        {'user_id': user_id, 'EMAIL': EMAIL, 'content': content})
    template = MIMEText(html.render(context=context), 'html')
    msg.attach(template)

    try:
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
    is_active = request.POST.get('is_active')
    housechore = HouseChore.objects.filter(id=id)[0]
    housechore.title = title
    housechore.description = description
    housechore.is_active = is_active
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
    if user.is_staff == True:
        messages.warning(
            request, f"ハウス管理者をdeactivateする事はできません。別のハウスメイトにハウス管理者権限の申請をしてもらい、譲渡してから自身をdeactivateください。/ You cannot deactivate the house administrator. Ask another housemate to apply for house administrator privileges, transfer it, and then deactivate yourself.")
        return redirect('users:manage')

    user.is_active = False
    user.save()
    messages.success(
        request, f"{email}をdeactivateしました。/ {email} has been deactivated.")
    return redirect('users:manage')
