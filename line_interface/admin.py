from django.contrib import admin
from .models import LineUser

class LineUserAdmin(admin.ModelAdmin):
    list_display = ['id','line_name','line_id','verify']

admin.site.register(LineUser, LineUserAdmin)