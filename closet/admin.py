from django.contrib import admin
from .models import ClosetImages, ClosetPost

class ClosetPostAdmin(admin.ModelAdmin):
    list_display = ['code', 'date', 'date_frame', 'description']

class ClosetImagesAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'thumbnail', 'src']

admin.site.register(ClosetPost, ClosetPostAdmin)
admin.site.register(ClosetImages, ClosetImagesAdmin)
