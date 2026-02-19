from django.contrib import admin
from .models import InteractiveWish, WishImage

class WishImageInline(admin.TabularInline):
    model = WishImage
    extra = 1 

@admin.register(InteractiveWish)
class InteractiveWishAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'receiver_name', 'slug', 'created_at')
    search_fields = ('sender_name', 'receiver_name', 'message')
    list_filter = ('created_at',)
    inlines = [WishImageInline]
    readonly_fields = ('slug', 'created_at')
