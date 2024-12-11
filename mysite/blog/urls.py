# Suggested code may be subject to a license. Learn more: ~LicenseLog:3771760657.
from django.urls import path
from .views import blog_list, blog_detail, blog_delete, blog_create, blog_update

urlpatterns = [
    path('', blog_list, name='blog_list'),
    path('create/', blog_create, name='blog_create'),
    path('<id>/update/', blog_update, name='blog_update'),
    path('<id>/', blog_detail, name='blog_detail'),
    path('<id>/delete/', blog_delete, name='blog_delete'),
    
]

