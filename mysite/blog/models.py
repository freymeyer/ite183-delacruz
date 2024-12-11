from django.db import models

# Create your models here.
class Post(models.Model):
# Suggested code may be subject to a license. Learn more: ~LicenseLog:1029435241.
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Suggested code may be subject to a license. Learn more: ~LicenseLog:617247860.
    def __str__(self):
        return self.title