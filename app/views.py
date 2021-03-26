from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from email.mime.text import MIMEText
import smtplib
from .models import HouseChore
from users.models import User
from atom.settings import DEBUG, DEFAULT_FROM_EMAIL, EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_POST


@login_required
def room(request):
    return render(request, 'app/room.html')


@login_required
def assign_chore(request):
    if request.method == 'POST':
        UserNum = User.objects.all().count()
        HouseChoreNum = HouseChore.objects.all().count()
        if UserNum == HouseChoreNum:
            random_housechore_list = HouseChore.objects.all(
            ).values_list('title', 'description').order_by('?')
            list_item = list(random_housechore_list)
            for i in range(UserNum):
                housemate = User.objects.order_by('id')[i]
                print(housemate)
                housemate.housechore_title = ''
                housemate.housechore_title = list_item[i][0]
                housemate.housechore_desc = ''
                housemate.housechore_desc = list_item[i][1]
                housemate.save()
            else:
                EMAIL = DEFAULT_FROM_EMAIL
                PASSWORD = EMAIL_HOST_PASSWORD
                for i in range(UserNum):
                    TO = (User.objects.all().values_list('email')[i][0])
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
                request, f"家事の数がオーバーしています。ハウスメイトの人数分まで家事を削除してください。/ The number of household chores is over. Delete up to the number of housemates.")
            if DEBUG:
                return redirect('http://127.0.0.1:8000/admin/')
            else:
                return redirect('https://glacial-shore-75579.herokuapp.com/admin/')

        return redirect('app:room')
