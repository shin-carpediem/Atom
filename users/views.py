from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            input_email = form.changed_data['email']
            input_password = form.changed_data['password']
            new_user = authenticate(email=input_email, password=input_password)
            if new_user is not None:
                login(request, new_user)
                # should change later
                return redirect('users:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})


def index(request):
    return render(request, 'users/index.html')
