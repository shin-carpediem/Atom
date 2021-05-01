from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'users'
urlpatterns = [
    path('index', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('pls_activate/', views.pls_activate, name='pls_activate'),
    path('signup/doing/', views.signup_doing, name='signup_doing'),
    path('signup/done/', views.signup_done, name='signup_done'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('', auth_views.LoginView.as_view(
        template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('request_house_owner', views.request_house_owner,
         name='request_house_owner'),
    path('inquire/', views.inquire, name='inquire'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('policy/', views.policy, name='policy'),
    path('terms/', views.terms, name='terms'),
    path('axes_locked/', views.axes_locked, name='axes_locked'),
    path('manage/', views.manage, name='manage'),
    path('manage/housemate/<int:housemate_id>/',
         views.housemate_detail, name='housemate_detail'),
    path('manage/housechore/<int:housechore_id>/',
         views.housechore_detail, name='housechore_detail'),
    path('manage/add_housechore', views.add_housechore, name='add_housechore'),
]
