from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import HouseChore


# Create your views here.
@login_required
def room(request):
    return render(request, 'app/room.html')


@login_required
def assign_chore(request):
    if request.method == 'POST':
        messages.success(request, f"割り振りに成功しました。")
        return redirect('app:room')
