from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from atom.settings import DEBUG
from .models import HouseChore
from users.models import User


# Create your views here.
@login_required
def room(request):
    return render(request, 'app/room.html')


@login_required
def assign_chore(request):
    if request.method == 'POST':
        # ハウスメイトの人数を算出
        UserNum = User.objects.all().count()
        # 家事の個数を算出
        HouseChoreNum = HouseChore.objects.all().count()
        # ハウスメイトの人数と家事の個数が一致するなら家事を割り振る
        if UserNum == HouseChoreNum:
            # 家事の並び順をシャッフルする
            random_housechore_list = HouseChore.objects.all(
            ).values_list('title', 'description').order_by('?')
            # titleのクエリセットからリストにする
            list_item = list(random_housechore_list)

            for i in range(UserNum):
                # i+1 番目のモデルの家事インスタンスを取得
                housemate = User.objects.get(id=1)
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
                messages.success(request, f"割り振りに成功しました。")

        elif UserNum > HouseChoreNum:
            messages.success(
                request, f"家事の数が足りません。家事をしなくてもいい人数分、「今週はなし」という家事を作成してください")
            if DEBUG:
                return redirect('http://127.0.0.1:8000/admin/')
            else:
                return redirect('https://glacial-shore-75579.herokuapp.com/')

        else:
            messages.success(
                request, f"家事の数がオーバーしています。ハウスメイトの人数分まで家事を削除してください。")
            if DEBUG:
                return redirect('http://127.0.0.1:8000/admin/')
            else:
                return redirect('https://glacial-shore-75579.herokuapp.com/')

        return redirect('app:room')
