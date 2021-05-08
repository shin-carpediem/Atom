from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.template import Context, Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from .models import HouseChore
from users.models import User, RequestChHouse
from users.forms import HouseChooseForm
from atom.settings import DEFAULT_FROM_EMAIL, EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_POST


# Create your views here.
@login_required
def room(request):
    user = request.user
    email = user.email
    house_choose_form = HouseChooseForm(request.POST or None)
    ctx = {
        'email': email,
        'house_choose_form': house_choose_form,
    }
    return render(request, 'app/room.html', ctx)


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
@staff_member_required
def assign_chore(request):
    if request.method == 'POST':
        housemates = User.objects.filter(
            house=request.user.house, is_active='True')
        # is_staff権限のユーザーのハウスと同じハウスメイト(is_active=true)の人数を算出
        UserNum = housemates.count()

        housechores = HouseChore.objects.filter(
            house=request.user.house, is_active='True')
        # is_staff権限のユーザーのハウスの家事の個数を算出
        HouseChoreNum = housechores.count()

        # ハウスメイトの人数と家事の個数が一致するなら家事を割り振る
        if UserNum == HouseChoreNum:
            # 家事の並び順をシャッフルする
            random_housechore_list = housechores.values_list(
                'title', 'description').order_by('?')
            # titleのクエリセットからリストにする
            list_item = list(random_housechore_list)

            for i in range(UserNum):
                # i+1 番目のモデルの家事インスタンスを取得
                housemate = housemates.order_by('id')[i]
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

                # NOTE:ここ処理めちゃ長くなっちゃうから、一列で表現できるようにする
                for i in range(UserNum):
                    target_users = User.objects.filter(
                        house=request.user.house, is_active='True')
                    TO = target_users.values_list('email')[i][0]
                    housemate_housechore_title = target_users.values_list('housechore_title')[
                        i][0]
                    housemate_housechore_desc = target_users.values_list('housechore_desc')[
                        i][0]

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
                      <p>Please check the housechore you are in charge of this week.</p>
                      <hr>
                      <p>家事のサマリ|Summary：{{ housemate_housechore_title }}</p>
                      <p>詳細|Description：{{ housemate_housechore_desc }}</p>
                      <hr>
                      <a href="https://atom-production.herokuapp.com/room">ページへ移動する / Go to page</a>
                      <br>
                      <p>Thank you.</p>
                    </body>
                    </html>
                    """

                    msg['Subject'] = '【Atom】今週の家事が割り振られました / This week’s housechore has been allocated'
                    msg['From'] = house_owner_email
                    msg['To'] = TO

                    html = Template(html)
                    context = Context({'housemate_housechore_title': housemate_housechore_title,
                                       'housemate_housechore_desc': housemate_housechore_desc})
                    # Attach parts into message container.
                    # According to RFC 2046, the last part of a multipart message, in this case
                    # the HTML message, is best and preferred.
                    template = MIMEText(html.render(context=context), 'html')
                    msg.attach(template)

                    try:
                        # access to the socket
                        s = smtplib.SMTP(EMAIL_HOST, EMAIL_POST)
                        s.starttls()
                        s.login(EMAIL, PASSWORD)
                        s.sendmail(EMAIL, TO, msg.as_string())
                        s.quit()
                        messages.success(
                            request, f"{TO}さんへの割り振りに成功しました。 / The allocation to {TO} was successful.")
                    except:
                        messages.warning(
                            request, f"{TO}さんへのメール送信に失敗しましたが、割り振りは完了しました。別途アナウンスをしてください。/ Email sending to {TO} failed, but allocation is complete. Please make a separate announcement.")

        elif UserNum > HouseChoreNum:
            messages.warning(
                request, f"家事の数が足りません。家事をしなくてもいい人数分、「今週はなし」という家事を作成してください。/ There are not enough housechore. Create a housechore called ”Nothing this week” for the number of people who do not have to do the housechore.")
            return redirect('users:manage')

        else:
            messages.warning(
                request, f"家事の数がオーバーしています。(メール認証が完了している)ハウスメイトの人数分まで家事を削除してください。/ The number of housechore is over. Delete up to the number of housemates (whose email verification has been completed).")
            return redirect('users:manage')

    return redirect('app:room')


@login_required
@staff_member_required
@require_POST
def reset_common_fee(request):
    Users = User.objects.filter(house=request.user.house, is_active='True')
    # すでに1人以上が共益費を支払い終えていたら、全員の共益費をリセットする関数を実行する。
    TrueUsersNum = Users.filter(done_monthly='True').count()
    if TrueUsersNum >= 1:
        UserNum = Users.count()
        for i in range(UserNum):
            housemate = Users.order_by('id')[i]
            housemate.done_monthly = False
            housemate.save()
        messages.success(
            request, f"ハウスメイト全員分の共益費支払いをリセットしました。/ It was successful in resetting common fee for all housemates.")
        return redirect('app:room')
    else:
        messages.warning(
            request, f"まだ誰も今月分の共益費を支払っていません。/ No one has paid this month's common service fee yet."
        )
        return render(request, 'app/room.html')


@login_required
@require_POST
def finish_task(request):

    try:
        user = User.objects.get(id=request.user.id)
        user_email = user.email
        user_housechore_title = user.housechore_title
        user_housechore_desc = user.housechore_desc

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
        user_done_weekly = user.done_weekly
        user_done_monthly = user.done_monthly

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
          <p>ハウスメイトの{{ user_email }}さんから家事完了の連絡を受けました。</p>
          <p>You received a notification from your housemate {{ user_email }} that he/she finised the housework.</p>
          <hr>
          <p>家事のサマリ|Summary：{{ user_housechore_title }}</p>
          <p>詳細|Description：{{ user_housechore_desc }}</p>
          <p>ステータス|Status：{{ user_done_weekly }}</p>
          <p>共益費の支払い完了|Completion of payment of common service fee：{{ user_done_monthly }}</p>
          <hr>
          <a href="https://atom-production.herokuapp.com/manage_top/">管理画面へ / Go to admin page</a>
          <br>
          <p>Thank you.</p>
        </body>
        </html>
        """

        html = Template(html)
        context = Context(
            {'user_email': user_email,
             'user_housechore_title': user_housechore_title,
             'user_housechore_desc': user_housechore_desc,
             'user_done_weekly': user_done_weekly,
             'user_done_monthly': user_done_monthly})
        template = MIMEText(html.render(context=context), 'html')
        msg.attach(template)

        try:
            s = smtplib.SMTP(EMAIL_HOST, EMAIL_POST)
            s.starttls()
            s.login(DEFAULT_FROM_EMAIL, PASSWORD)
            s.sendmail(EMAIL, TO, msg.as_string())
            s.quit()

            messages.success(
                request, f"報告できました。/ The report was successful.")
        except:
            messages.warning(
                request, f"メール送信に失敗しましたが、ステータスは変更できました。/ Failed to send an email, but your status has been successfully changed.")

    except:
        messages.warning(
            request, f"まだハウス管理者がいないようです。/ It seems that there is no house manager yet.")
    return redirect('app:room')


@login_required
@require_POST
def request_ch_house(request):
    user = request.user
    current_house = user.house
    request_house = request.POST.get('name')
    RequestChHouse(email=user.email, current_house=current_house,
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
      <p>ユーザー（ユーザーID：{{ user.id }}）（メールアドレス：{{ user.email }}）からハウス変更の申請が届きました。</p>
      <hr>
      <p>現在のハウス:{{ current_house }}</p>
      <p>新しく設定したいハウス:{{ request_house }}</p>
      <hr>
      <a href="https://atom-production.herokuapp.com/manage_top/">管理画面へ</a>
      <br>
      <p>Thank you.</p>
    </body>
    </html>
    """

    html = Template(html)
    context = Context(
        {'user.id': user.id,
         'user.email': user.email,
         'current_house': current_house,
         'request_house': request_house})
    template = MIMEText(html.render(context=context), 'html')
    msg.attach(template)

    try:
        s = smtplib.SMTP(EMAIL_HOST, EMAIL_POST)
        s.starttls()
        s.login(DEFAULT_FROM_EMAIL, PASSWORD)
        s.sendmail(EMAIL, TO, msg.as_string())
        s.quit()
        messages.success(
            request, f"ハウス変更の申請が完了しました。 / The application for changing the house has been completed.")
    except:
        messages.warning(
            request, f"メール送信に失敗しました。しばらくしてもう一度お試しください。/ Failed to send the email. Please try again after a while."
        )

    return redirect('users:index')
