from django.contrib import admin
from .models import MangaReadingList
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
admin.site.register(MangaReadingList)
admin.site.register(CustomUser)

