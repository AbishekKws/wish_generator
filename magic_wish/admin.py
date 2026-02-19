from .models import MusicCategory, MusicLibrary, Wish, WishImage, CelebrationTemplate
from django.utils.html import format_html
from .models import CelebrationTemplate
from django.contrib import admin
from django import forms

TEMPLATE_CHOICES = [
    ('heart_shape', 'Romantic Heart'),
    ('floating_photos', 'Floating Memories'),
    ('colorful_magic', 'Color Blast'),
    ('balloon_parade', 'Balloon Parade'),
    ('falling_leaves', 'Autumn Whisper'),
    ('matrix_rain', 'Matrix Digital'),
    ('snowy_winter', 'Snowy Winter'),
    ('firework_show', 'Firework Show'),
    ('sakura_bloom', 'Sakura Bloom'),
    ('space_odyssey', 'Space Odyssey'),
    ('retro_polaroid', 'Retro Polaroid'),
    ('golden_luxury', 'Golden Luxury'),
    ('underwater_vibes', 'Underwater World'),
    ('glitch_art', 'Cyber Glitch'),
    ('comic_pop', 'Comic Book Pop'),
    ('neon_pulse', 'Neon Pulse'),
    ('festival_lights', 'Festival Lights'),
    ('golden_glitter', 'Golden Glitter Magic'),
]

class CelebrationTemplateAdminForm(forms.ModelForm):
    template_id = forms.ChoiceField(choices=TEMPLATE_CHOICES, label="Template ID")

    class Meta:
        model = CelebrationTemplate
        fields = '__all__'

@admin.register(CelebrationTemplate)
class CelebrationTemplateAdmin(admin.ModelAdmin):
    form = CelebrationTemplateAdminForm 
    
    list_display = ('name', 'template_id', 'display_preview')
    search_fields = ('name', 'template_id')
    list_filter = ('template_id',)

    def display_preview(self, obj):
        if obj.preview_image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 8px; object-fit: cover;" />', obj.preview_image.url)
        return "No Image"
    
    display_preview.short_description = 'Preview'

    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'template_id')
        }),
        ('Media Assets', {
            'fields': ('preview_image',),
            'description': 'Upload a preview image here. If left blank, the system will use the static folder image.'
        }),
    )

class WishImageInline(admin.TabularInline):
    model = WishImage
    extra = 1 

@admin.register(MusicCategory)
class MusicCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(MusicLibrary)
class MusicLibraryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    list_filter = ('category',)
    search_fields = ('title',)

@admin.register(Wish)
class WishAdmin(admin.ModelAdmin):
    list_display = ('receiver_name', 'sender_name', 'wish_type', 'created_at')
    list_filter = ('wish_type', 'created_at')
    search_fields = ('sender_name', 'receiver_name', 'message')
    inlines = [WishImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('wish_type', 'template_name')
        }),
        ('Personal Details', {
            'fields': ('sender_name', 'receiver_name', 'message')
        }),
        ('Music Selection', {
            'fields': ('selected_music', 'custom_music'),
            'description': "Choose a library song OR upload a custom file."
        }),
    )
