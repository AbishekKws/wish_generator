from django.db import models
import uuid

class BirthdayWish(models.Model):
    # Unique slug for sharing 
    slug = models.SlugField(unique=True, default=uuid.uuid4, editable=False)
    sender_name = models.CharField(max_length=100)
    receiver_name = models.CharField(max_length=100)
    message = models.TextField()
    music = models.FileField(upload_to='birthday_music/', null=True, blank=True)
    
    # --- SEO/Social Sharing ---
    template_name = models.CharField(max_length=50, default="default")
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wish for {self.receiver_name} from {self.sender_name}"

class WishImage(models.Model):
    wish = models.ForeignKey(BirthdayWish, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='birthday_memories/')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.wish.receiver_name}"