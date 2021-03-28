from django.contrib import admin
from .models import HouseChore


# # Register your models here.
class HouseChoreAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'house']
    list_display = ('title', 'description', 'house')
    list_editable = ('house', )
    list_filter = ('house', )
    search_fields = ('house', )
    ordering = ('title', )


admin.site.register(HouseChore, HouseChoreAdmin)
