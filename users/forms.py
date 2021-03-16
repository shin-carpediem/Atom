# settings.py の AUTH_USER_MODEL に設定したモデルを呼び出す
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email',)
    captcha = ReCaptchaField(widget=ReCaptchaWidget())
