from django import forms
from django.forms import fields
from .models import HouseChore
from django.utils.translation import gettext as _


class AddHousechoreForm(forms.ModelForm):
    class Meta:
        model = HouseChore
        fields = ('title', 'description',)
