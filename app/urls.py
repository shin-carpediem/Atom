from django.urls import path
from . import views


app_name = 'app'
urlpatterns = [
    path('room', views.room, name='room'),
    path('assign_chore', views.assign_chore, name='assign_chore'),
    path('finish_task', views.finish_task, name='finish_task'),
    path('request_house_owner', views.request_house_owner,
         name='request_house_owner'),
]
