from django.db import models
import uuid

class InteractiveWish(models.Model):
    # Unique slug for private sharing
    slug = models.SlugField(unique=True, default=uuid.uuid4, editable=False)
    
    sender_name = models.CharField(max_length=100)
    receiver_name = models.CharField(max_length=100)
    message = models.TextField()
    music = models.FileField(upload_to='wish_music/', blank=True, null=True)
    
    # --- SEO & Analytics Fields ---
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender_name} to {self.receiver_name}"

class WishImage(models.Model):
    wish = models.ForeignKey(InteractiveWish, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='wish_photos/')

    def __str__(self):
        return f"Image for {self.wish.receiver_name}"