from django.urls import path
from . import views


app_name = 'app'
urlpatterns = [
    path('room', views.room, name='room'),
    path('assign_chore', views.assign_chore, name='assign_chore'),
]
