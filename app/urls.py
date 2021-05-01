from django.urls import path
from . import views


app_name = 'app'
urlpatterns = [
    path('room', views.room, name='room'),
    path('set_username', views.set_username, name='set_username'),
    path('assign_chore', views.assign_chore, name='assign_chore'),
    path('reset_common_fee', views.reset_common_fee, name='reset_common_fee'),
    path('finish_task', views.finish_task, name='finish_task'),
    path('request_ch_house', views.request_ch_house, name='request_ch_house'),
]
