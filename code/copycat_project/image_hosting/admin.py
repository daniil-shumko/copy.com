from django.contrib import admin
from image_hosting.models import Category, Image


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'caption', 'category', 'timestamp')


class CatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Category, CatAdmin)
admin.site.register(Image, ImageAdmin)