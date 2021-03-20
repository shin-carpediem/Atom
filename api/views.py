from django.shortcuts import render
from django.contrib.auth.models import UserManager
import django_filters
from rest_framework import viewsets, filters
from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from users.models import User, House
from app.models import HouseChore
from .serializer import UserSerializer, HouseSerializer, HouseChoreSerializer


# Create your views here.
# users
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer


class HouseChoreViewSet(viewsets.ModelViewSet):
    queryset = HouseChore.objects.all()
    serializer_class = HouseChoreSerializer