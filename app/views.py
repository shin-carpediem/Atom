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
        housechore_list = HouseChore.objects.all().values_list('title', flat=True)
        print(housechore_list)
        print(housechore_list[0])
        # housemate_title = housechore_list.title
        # print(housemate_title)
        housemate_list = User.objects.all().values_list('housechore', flat=True)
        print(housemate_list)
        print(housemate_list[0])
        # housechore_list[0] = housemate_list[0]
        # User.housechore = housechore_list
        # User.save()
        messages.success(request, f"割り振りに成功しました。")
        return redirect('app:room')
