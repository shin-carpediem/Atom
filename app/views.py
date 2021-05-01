from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
from .models import HouseChore
from users.models import User, RequestChHouse
from users.forms import HouseChooseForm
from atom.settings import DEBUG, DEFAULT_FROM_EMAIL, EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_POST


# Create your views here.
@login_required
def room(request):
    house_choose_form = HouseChooseForm(request.POST or None)
    return render(request, 'app/room.html', {'house_choose_form': house_choose_form})


@login_required
def set_username(request):
    user = User.objects.get(id=request.user.id)
    name = request.GET.get(key='name')
    user.name = name
    user.save()
    messages.success(
        request, f"ユーザーネームを{name}に設定しました。 / You set your username to {name}.")
    return redirect('app:room')


@login_required
def assign_chore(request):
    if request.method == 'POST':
        # is_staff権限のユーザーのハウスと同じハウスメイト(is_active=true)の人数を算出
        UserNum = User.objects.filter(
            house=request.user.house, is_active='True').count()
        # is_staff権限のユーザーのハウスの家事の個数を算出
        HouseChoreNum = HouseChore.objects.filter(
            house=request.user.house).count()
        # ハウスメイトの人数と家事の個数が一致するなら家事を割り振る
        if UserNum == HouseChoreNum:
            # 家事の並び順をシャッフルする
            random_housechore_list = HouseChore.objects.filter(
                house=request.user.house, is_active=True).values_list('title', 'description').order_by('?')
            # titleのクエリセットからリストにする
            list_item = list(random_housechore_list)

            for i in range(UserNum):
                # i+1 番目のモデルの家事インスタンスを取得
                housemate = User.objects.filter(
                    house=request.user.house, is_active='True').order_by('id')[i]
                # ハウスメイトの家事実施状況をyetにする
                housemate.done_weekly = False
                # i+1 番目のモデルの家事インスタンスを一旦削除
                housemate.housechore_title = ''
                # i 番目のモデルの家事インスタンスに、Aを代入
                housemate.housechore_title = list_item[i][0]

                # 家事モデルのdescフィールドも
                # Userモデルhousechore_descフィールドに連動させる
                housemate.housechore_desc = ''
                housemate.housechore_desc = list_item[i][1]
                housemate.save()

            # forルーブが終わりまで実行された後に行われる処理
            else:
                EMAIL = DEFAULT_FROM_EMAIL
                PASSWORD = EMAIL_HOST_PASSWORD

                house_owner_email = User.objects.filter(
                    house=request.user.house, is_active='True', is_staff='True').values_list('email')[0][0]

                # TODO:ここ処理めちゃ長くなっちゃうから、一列で表現できるようにする
                for i in range(UserNum):
                    TO = (User.objects.filter(
                        house=request.user.house, is_active='True').values_list('email')[i][0])

                    msg = MIMEMultipart('alternative')
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
                      <p>今週の自分が担当する家事をご確認ください。</p>
                      <a href="https://atom-production.herokuapp.com/room">家事を確認する</a>
                      <br><br>
                      <p>Please check the housework you are in charge of this week.</p>
                      <a href="https://atom-production.herokuapp.com/room">Check my housechore</a>
                      <br>
                      <p>Thank you.</p>
                      <hr>
                      <img style="padding:5px 5px 0px 0px; float:left; width:20px;" src="cid:{logo_image}" alt="Logo">
                      <p style="color:#609bb6;">From Atom team</p>
                      </div>
                    </body>
                    </html>
                    """

                    msg['Subject'] = '【Atom】今週の家事が割り振られました / This week’s housework has been allocated'
                    msg['From'] = house_owner_email
                    msg['To'] = TO

                    fp = open('static/img/users/icon.png', 'rb')
                    img = MIMEImage(fp.read())
                    fp.close()
                    # Define the image's ID as referenced above
                    img.add_header('Content-ID', '<logo_image>')
                    msg.attach(img)

                    # Attach parts into message container.
                    # According to RFC 2046, the last part of a multipart message, in this case
                    # the HTML message, is best and preferred.
                    template = MIMEText(html, 'html')
                    msg.attach(template)

                    # access to the socket
                    s = smtplib.SMTP(EMAIL_HOST, EMAIL_POST)
                    s.starttls()
                    s.login(EMAIL, PASSWORD)
                    s.sendmail(EMAIL, TO, msg.as_string())
                    s.quit()
                messages.success(
                    request, f"割り振りに成功しました。 / The allocation was successful.")

        elif UserNum > HouseChoreNum:
            messages.warning(
                request, f"家事の数が足りません。家事をしなくてもいい人数分、「今週はなし」という家事を作成してください。/ There are not enough housework. Create a housework called ”Nothing this week” for the number of people who do not have to do the housework.")
            return redirect('users:manage')

        else:
            messages.warning(
                request, f"家事の数がオーバーしています。(メール認証が完了している)ハウスメイトの人数分まで家事を削除してください。/ The number of household chores is over. Delete up to the number of housemates (whose email verification has been completed).")
            return redirect('users:manage')

    return redirect('app:room')


@login_required
def reset_common_fee(request):
    if request.method == 'POST':
        UserNum = User.objects.filter(
            house=request.user.house, is_active='True').count()
        for i in range(UserNum):
            housemate = User.objects.filter(
                house=request.user.house, is_active='True').order_by('id')[i]
            housemate.done_monthly = False
            housemate.save()
        messages.success(
            request, f"ハウスメイト全員分の共益費支払いをリセットしました。/ It was successful in resetting common fee for all housemates.")
    return redirect('app:room')


@login_required
@require_POST
def finish_task(request):

    try:
        user = User.objects.get(id=request.user.id)

        values = request.POST.getlist('task')
        if 'weekly' in values and 'monthly' in values:
            user.done_weekly = True
            user.done_monthly = True
        elif 'weekly' in values:
            user.done_weekly = True
        elif 'monthly' in values:
            user.done_monthly = True
        else:
            messages.warning(
                request, f"チェックボックスにチェックを入れてください。/ Please check the check box.")
            return render(request, 'app/room.html')

        user.save()

        EMAIL = request.user.email
        PASSWORD = EMAIL_HOST_PASSWORD
        TO = User.objects.filter(house=request.user.house, is_active='True',
                                 is_staff='True').values_list('email')[0][0]

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '【Atom】ハウスメイトから家事完了の連絡を受けました'
        msg['From'] = EMAIL
        msg['To'] = TO

        # Create the body of the message (a plain-text and an HTML version).
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
          <p>ハウスメイトから家事完了の連絡を受けました。</p>
          <a href="https://atom-production.herokuapp.com/manage/">管理画面へ</a>
          <br><br>
          <p>You received a notification from your housemate that he/she finised the housework.</p>
          <a href="https://atom-production.herokuapp.com/manage/">Go to admin page</a>
          <br>
          <p>Thank you.</p>
          <hr>
          <img style="padding:5px 5px 0px 0px; float:left; width:20px;" src="cid:{logo_image}" alt="Logo">
          <p style="color:#609bb6;">From Atom team</p>
        </body>
        </html>
        """

        fp = open('static/img/users/icon.png', 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        # Define the image's ID as referenced above
        img.add_header('Content-ID', '<logo_image>')
        msg.attach(img)

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        template = MIMEText(html, 'html')
        msg.attach(template)

        # access to the socket
        s = smtplib.SMTP(EMAIL_HOST, EMAIL_POST)
        s.starttls()
        s.login(DEFAULT_FROM_EMAIL, PASSWORD)
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        s.sendmail(EMAIL, TO, msg.as_string())
        s.quit()

        messages.success(request, f"報告できました。/ The a report was successful.")

    except:
        messages.warning(
            request, f"まだハウス管理者がいないようです。/ It seems that there is no house manager yet.")
    return redirect('app:room')


@login_required
@require_POST
def request_ch_house(request):
    user = request.user
    request_house = request.POST.get('name')
    RequestChHouse(email=user.email, current_house=user.house,
                   request_house=request_house).save()

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
      <a href="https://atom-production.herokuapp.com/manage/">管理画面へ</a>
      <br>
      <p>Thank you.</p>
      <hr>
      <img style="padding:5px 5px 0px 0px; float:left; width:20px;" src="cid:{logo_image}" alt="Logo">
      <p style="color:#609bb6;">From Atom team</p>
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
        request, f"ハウス変更の申請が完了しました。 / The application for changing the house has been completed.")

    return redirect('users:index')
