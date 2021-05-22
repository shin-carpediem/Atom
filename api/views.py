from django.shortcuts import render
from django.contrib.auth.models import UserManager
import django_filters
from rest_framework import viewsets, filters
from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from users.models import House, User, Inquire, RequestChHouse, RequestHouseOwner
from app.models import HouseChore
from .serializer import HouseSerializer, UserSerializer, InquireSerializer, RequestChHouseSerializer, RequestHouseOwnerSerializer, HouseChoreSerializer


# Create your views here.
class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class InquireViewSet(viewsets.ModelViewSet):
    queryset = Inquire.objects.all()
    serializer_class = InquireSerializer


class RequestChHouseViewSet(viewsets.ModelViewSet):
    queryset = RequestChHouse.objects.all()
    serializer_class = RequestChHouseSerializer


class RequestHouseOwnerViewSet(viewsets.ModelViewSet):
    queryset = RequestHouseOwner.objects.all()
    serializer_class = RequestHouseOwnerSerializer


class HouseChoreViewSet(viewsets.ModelViewSet):
    queryset = HouseChore.objects.all()
    serializer_class = HouseChoreSerializer