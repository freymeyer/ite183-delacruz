# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser
    Allows for additional user-specific fields if needed
    """
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    def __str__(self):
        return self.username

class MangaReadingList(models.Model):
    """
    Model to track user's manga reading progress
    """
    STATUS_CHOICES = [
        ('plan_to_read', 'Plan to Read'),
        ('reading', 'Reading'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('dropped', 'Dropped')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='manga_list')
    manga_id = models.IntegerField()  # MAL Manga ID
    manga_title = models.CharField(max_length=255)
    manga_image_url = models.URLField(blank=True, null=True)
    
    reading_status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='plan_to_read'
    )
    
    num_volumes_read = models.IntegerField(
        default=0, 
        validators=[MinValueValidator(0)]
    )
    
    num_chapters_read = models.IntegerField(
        default=0, 
        validators=[MinValueValidator(0)]
    )
    
    user_rating = models.FloatField(
        blank=True, 
        null=True, 
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    
    user_review = models.TextField(blank=True, null=True)
    
    started_reading_date = models.DateField(blank=True, null=True)
    completed_reading_date = models.DateField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'manga_id']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}'s {self.manga_title}"