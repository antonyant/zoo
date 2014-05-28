from django.contrib import admin
from models import GalleryType, GalleryOrder, PhotoOrder


class PhotoInline(admin.TabularInline):
    model = PhotoOrder


class GalleryOrderAdmin(admin.ModelAdmin):
    list_display = ['gallery', 'active','gallery_type', 'order', 'hero_image']
    list_editable = ['gallery_type', 'order', 'hero_image', 'active']
    inlines = [PhotoInline]


class GalleryInline(admin.TabularInline):
    model = GalleryOrder
   

class GalleryTypeAdmin(admin.ModelAdmin):
    inlines = [GalleryInline]


admin.site.register(GalleryType, GalleryTypeAdmin)
admin.site.register(GalleryOrder, GalleryOrderAdmin)
