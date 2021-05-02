from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from .models import HouseChore


# # Register your models here.
@admin.register(HouseChore)
class HouseChoreAdmin(GuardedModelAdmin):
    fields = ['title', 'description', 'house', 'is_active']
    list_display = ('title', 'description', 'house', 'is_active')
    list_filter = ('house', )
    search_fields = ('house', )
    ordering = ('title', )
