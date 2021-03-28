from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from guardian.admin import GuardedModelAdmin
from .models import User, House


# Register your models here.
class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', )


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name',
                           'house', 'housechore_title', 'housechore_desc')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
                                       'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide', ), 'fields': (
            'email', 'name', 'house', 'password1', 'password2'), }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('email', 'name', 'house', 'housechore_title', 'housechore_desc', 'is_staff',
                    'is_superuser', 'is_active')
    list_editable = ('house', 'is_staff')
    list_filter = ('house', 'is_staff', 'is_active', 'groups')
    search_fields = ('email', )
    ordering = ('email', )


@admin.register(House)
class HouseAdmin(GuardedModelAdmin):
    fields = ['name']
    list_display = ('name', 'created_at')
    search_fields = ('name', )
    ordering = ('name', )


admin.site.register(User, MyUserAdmin)
