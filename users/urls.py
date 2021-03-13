from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'users'
urlpatterns = [
    path('index', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('pls_activate/', views.pls_activate, name='pls_activate'),
    path('signup/done/', views.signup_done, name='signup_done'),
    path('', auth_views.LoginView.as_view(
        template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LoginView.as_view(), name=('logout')),
]
