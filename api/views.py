from django.shortcuts import render
from django.contrib.auth.models import UserManager
import django_filters
from rest_framework import viewsets, filters
from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from users.models import User
from .serializer import UserSerializer


# Create your views here.
# users
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
