from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from guardian.admin import GuardedModelAdmin
from .models import User, House, Inquire, RequestChHouse, RequestHouseOwner


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
                           'house', 'house_common_fee', 'house_common_fee_date', 'housechore_title', 'housechore_desc', 'done_weekly', 'done_monthly')}),
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
    list_display = ('email', 'name', 'house', 'house_common_fee', 'house_common_fee_date', 'housechore_title', 'housechore_desc', 'done_weekly', 'done_monthly', 'is_staff',
                    'is_superuser', 'is_active')
    list_editable = ('house', 'house_common_fee',
                     'house_common_fee_date', 'done_weekly', 'done_monthly')
    list_filter = ('house', 'house_common_fee', 'house_common_fee_date', 'done_weekly', 'done_monthly',
                   'is_staff', 'is_active', 'groups')
    search_fields = ('email', )
    ordering = ('email', )


@admin.register(House)
class HouseAdmin(GuardedModelAdmin):
    fields = ['name', 'common_fee', 'common_fee_date']
    list_display = ('name', 'common_fee', 'common_fee_date', 'created_at')
    search_fields = ('name', )
    ordering = ('name', )


@admin.register(Inquire)
class InquireAdmin(GuardedModelAdmin):
    fields = ['email', 'session', 'content']
    list_display = ('email', 'session', 'content', 'created_at')
    search_fields = ('email', )
    ordering = ('email', )


@admin.register(RequestChHouse)
class RequestChHouseAdmin(GuardedModelAdmin):
    fields = ['email', 'current_house', 'request_house']
    list_display = ('email', 'current_house', 'request_house', 'created_at')
    search_fields = ('email', )
    ordering = ('email', )


@admin.register(RequestHouseOwner)
class RequestHouseOwnerAdmin(GuardedModelAdmin):
    fields = ['email', 'house']
    list_display = ('email', 'house', 'created_at')
    search_fields = ('email', )
    ordering = ('email', )


admin.site.register(User, MyUserAdmin)
