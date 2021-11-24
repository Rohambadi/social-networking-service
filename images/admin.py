from django.contrib import admin
from .models import Image


@admin.register(Image)
class imageAdmin(admin.ModelAdmin):
    list_display = ['user', 'image', 'title', 'description', 'created']
