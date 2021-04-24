from django import forms
# settings.py の AUTH_USER_MODEL に設定したモデルを呼び出す
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext as _
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from . import utils
from .models import House


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email',)
    captcha = ReCaptchaField(widget=ReCaptchaWidget())


class HouseChooseForm(forms.Form):
    name = forms.ModelChoiceField(
        queryset=House.objects.all(), empty_label=_("選択してください"))


class TwoStepAuthForm(AuthenticationForm):
    token = forms.CharField(max_length=254, label=_("ワンタイムパスワード"))

    def confirm_login_allowed(self, user):
        if utils.get_token(user) != self.cleaned_data.get('token'):
            raise forms.ValidationError(
                _("Google Authenticatorの結果と合致しませんでした。")
            )
        super().confirm_login_allowed(user)
