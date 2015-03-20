from django.contrib import admin
from image_hosting.models import Category, Image


class ImageAdmin(admin.ModelAdmin):
    list_display = ('url_image_name', 'caption', 'category')


admin.site.register(Category)
admin.site.register(Image, ImageAdmin)