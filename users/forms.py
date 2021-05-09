from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db.models import query
from django.forms import fields
from django.utils.translation import gettext as _
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
        queryset=House.objects.all(), empty_label=_("選択してください"))
