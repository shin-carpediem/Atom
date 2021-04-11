from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from email.mime.text import MIMEText
import smtplib
from .models import HouseChore
from users.models import User
from atom.settings import DEBUG, DEFAULT_FROM_EMAIL, EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_POST


# Create your views here.
@login_required
def room(request):
    return render(request, 'app/room.html')


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
                house=request.user.house).values_list('title', 'description').order_by('?')
            # titleのクエリセットからリストにする
            list_item = list(random_housechore_list)

            for i in range(UserNum):
                # i+1 番目のモデルの家事インスタンスを取得
                housemate = User.objects.filter(
                    house=request.user.house, is_active='True').order_by('id')[i]
                print(housemate)
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

                # TODO:ここ処理めちゃ長くなっちゃうから、一列で表現できるようにする
                for i in range(UserNum):
                    TO = (User.objects.filter(
                        house=request.user.house, is_active='True').values_list('email')[i][0])

                    if DEBUG:
                        msg = MIMEText(
                            '今週の自分が担当する家事をご確認ください。\n'
                            '\n'
                            'http://127.0.0.1:8000/room\n'
                            '\n'
                            '\n'
                            '\n'
                            'Please check the housework you are in charge of this week. \n'
                            '\n'
                            'http://127.0.0.1:8000/room\n'
                            '\n'
                        )
                    else:
                        msg = MIMEText(
                            '今週の自分が担当する家事をご確認ください。\n'
                            '\n'
                            'https://glacial-shore-75579.herokuapp.com/room\n'
                            '\n'
                            '\n'
                            '\n'
                            'Please check the housework you are in charge of this week. \n'
                            '\n'
                            'https://glacial-shore-75579.herokuapp.com/room\n'
                            '\n'
                        )
                    msg['Subject'] = '【Atom】今週の家事が割り振られました / This week’s housework has been allocated'
                    msg['From'] = DEFAULT_FROM_EMAIL
                    msg['To'] = TO

                    # access to the socket
                    s = smtplib.SMTP(EMAIL_HOST, EMAIL_POST)
                    s.starttls()
                    s.login(EMAIL, PASSWORD)
                    s.sendmail(EMAIL, TO, msg.as_string())
                    s.quit()
                messages.success(
                    request, f"割り振りに成功しました。 / The allocation was successful.")

        elif UserNum > HouseChoreNum:
            messages.success(
                request, f"家事の数が足りません。家事をしなくてもいい人数分、「今週はなし」という家事を作成してください。/ There are not enough housework. Create a housework called ”Nothing this week” for the number of people who do not have to do the housework.")
            if DEBUG:
                return redirect('http://127.0.0.1:8000/admin/')
            else:
                return redirect('https://glacial-shore-75579.herokuapp.com/admin/')

        else:
            messages.success(
                request, f"家事の数がオーバーしています。(メール認証が完了している)ハウスメイトの人数分まで家事を削除してください。/ The number of household chores is over. Delete up to the number of housemates (whose email verification has been completed).")
            if DEBUG:
                return redirect('http://127.0.0.1:8000/admin/')
            else:
                return redirect('https://glacial-shore-75579.herokuapp.com/admin/')

    return redirect('app:room')


@login_required
def request_house_owner(request):
    EMAIL = request.user.email
    PASSWORD = EMAIL_HOST_PASSWORD
    TO = DEFAULT_FROM_EMAIL

    if DEBUG:
        msg = MIMEText(
            'ユーザーからハウス管理者権限の申請が届きました。\n'
            '\n'
            'is_staffをTrueにしてください。\n'
            '\n'
            'http://127.0.0.1:8000/admin/\n'
            '\n'
        )
    else:
        msg = MIMEText(
            'ユーザーからハウス管理者権限の申請が届きました。\n'
            '\n'
            'is_staffをTrueにしてください。\n'
            '\n'
            'https://glacial-shore-75579.herokuapp.com/admin/\n'
            '\n'
        )
    msg['Subject'] = '【Atom】ユーザーからハウス管理者権限の申請が届きました'
    msg['From'] = EMAIL
    msg['To'] = TO

    # access to the socket
    s = smtplib.SMTP(EMAIL_HOST, EMAIL_POST)
    s.starttls()
    s.login(DEFAULT_FROM_EMAIL, PASSWORD)
    s.sendmail(EMAIL, TO, msg.as_string())
    s.quit()
    messages.success(
        request, f"ハウス管理者権限の申請が完了しました / Application for house administrator authority has been completed.")

    return render(request, 'app/room.html')
