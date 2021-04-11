from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from .models import HouseChore


# # Register your models here.
@admin.register(HouseChore)
class HouseChoreAdmin(GuardedModelAdmin):
    fields = ['title', 'description', 'house']
    list_display = ('title', 'description', 'house')
    list_editable = ('description', )
    list_filter = ('house', )
    search_fields = ('house', )
    ordering = ('title', )
