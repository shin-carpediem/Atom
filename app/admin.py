from django.contrib import admin
from .models import HouseChore


# # Register your models here.
# class HouseChoreAdmin(admin.ModelAdmin):
#     list_display = ('title', 'description', 'house')
#     list_editable = ('title', 'description')
#     ordering = ('house', )


admin.site.register(HouseChore)
