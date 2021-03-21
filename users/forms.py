from django import forms
# settings.py の AUTH_USER_MODEL に設定したモデルを呼び出す
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from .models import House


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email',)
    captcha = ReCaptchaField(widget=ReCaptchaWidget())


class HouseChooseForm(forms.Form):
    name = forms.ModelChoiceField(
        queryset=House.objects.all(), empty_label="選択してください")
