from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import HouseChore
from users.models import User


# Create your views here.
@login_required
def room(request):
    return render(request, 'app/room.html')


@login_required
def assign_chore(request):
    if request.method == 'POST':
        # 家事の並び順をシャッフルする
        random_housechore_list = HouseChore.objects.all(
        ).values_list('title', 'description').order_by('?')
        # titleのクエリセットからリストにする
        list_item = list(random_housechore_list)

        # ハウスメイトの人数を算出
        UserNum = User.objects.all().count()

        for i in range(UserNum):
            # i+1 番目のモデルの家事インスタンスを取得
            housemate = User.objects.get(id=i+1)
            # i+1 番目のモデルの家事インスタンスを一旦削除
            housemate.housechore_title = ''
            # i 番目のモデルの家事インスタンスに、Aを代入
            housemate.housechore_title = list_item[i][0]

            # 家事モデルのdescフィールドも
            # Userモデルhousechore_descフィールドに連動させる
            housemate.housechore_desc = ''
            housemate.housechore_desc = list_item[i][1]
            housemate.save()

        messages.success(request, f"割り振りに成功しました。")
        return redirect('app:room')
