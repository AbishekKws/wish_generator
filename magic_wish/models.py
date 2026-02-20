from django.db import models
from django.utils.text import slugify
import uuid

# Music Category (e.g., Birthday, Sad, Romantic, Devotional)
class MusicCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Music Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Pre-uploaded songs for users to choose from
class MusicLibrary(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(MusicCategory, on_delete=models.CASCADE, related_name='musics')
    audio_file = models.FileField(upload_to='music_collection/')
    
    def __str__(self):
        return f"{self.title} - ({self.category.name})"

# The Main Wish Model (Dynamic Version)
class Wish(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # SEO Friendly URL (Slug)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, db_index=True)
    
    # Platform Logic
    wish_type = models.CharField(max_length=50, default='birthday') 
    template_name = models.CharField(max_length=50, default='heart_shape')
    
    # User Details
    sender_name = models.CharField(max_length=100)
    receiver_name = models.CharField(max_length=100)
    message = models.TextField()
    
    # SEO Fields (थपिएको - Search Engine Optimization को लागि)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(max_length=200, blank=True, null=True)
    
    # Hybrid Music Support
    selected_music = models.ForeignKey(MusicLibrary, on_delete=models.SET_NULL, null=True, blank=True)
    custom_music = models.FileField(upload_to='custom_music/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Slug Generate गर्ने
        if not self.slug:
            base_slug = slugify(f"{self.wish_type} wish for {self.receiver_name}")
            self.slug = f"{base_slug}-{str(self.id)[:8]}"
        
        # SEO Meta Title Generate गर्ने
        if not self.meta_title:
            self.meta_title = f"✨ Special {self.wish_type.capitalize()} Surprise for {self.receiver_name} | Surprise Me"
        
        # SEO Meta Description Generate गर्ने
        if not self.meta_description:
            self.meta_description = f"{self.sender_name} has created a magical {self.wish_type} digital surprise for {self.receiver_name}. Open the link to see the message!"
            
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.wish_type} wish for {self.receiver_name}"

class CelebrationTemplate(models.Model):
    template_id = models.CharField(max_length=50, unique=True) # e.g., 'heart_shape'
    name = models.CharField(max_length=100)
    preview_image = models.ImageField(upload_to='template_previews/', null=True, blank=True)

    def __str__(self):
        return self.name

# Multiple Images for the Wish
class WishImage(models.Model):
    wish = models.ForeignKey(Wish, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='wish_images/')
    alt_text = models.CharField(max_length=255, blank=True, null=True) # SEO को लागि थपिएको

    def save(self, *args, **kwargs):
        if not self.alt_text:
            self.alt_text = f"Surprise image for {self.wish.receiver_name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.wish.receiver_name}"


class VisitorIP(models.Model):
    ip_address = models.GenericIPAddressField()
    visited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} on {self.visited_at}"

class VisitorCount(models.Model):
    total_visits = models.PositiveIntegerField(default=0)

class Rating(models.Model):
    score = models.IntegerField(default=5) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.score} Stars"