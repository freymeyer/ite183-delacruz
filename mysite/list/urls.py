from django.urls import path
from . import views
from .views import (
    fetch_manga_list, 
    add_to_list, 
    register_user, 
    login_view, 
    logout_view, 
    my_manga_list,
    update_manga_list_entry,
    home_view
)

urlpatterns = [
    path('', home_view, name='home'),
    
    # Manga List Routes
    path('mangalist/', fetch_manga_list, name='manga_list'),
    path('add_to_list/', add_to_list, name='add_to_list'),
    
    # Authentication Routes
    path('accounts/register/', register_user, name='register'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    
    # User Manga List Routes
    path('my-manga-list/', my_manga_list, name='my_manga_list'),
    path('my-manga-list/update/<int:entry_id>/', views.update_manga_list_entry, name='update_manga_entry'),
    path('delete_manga_entry/<int:entry_id>/', views.delete_manga_list_entry, name='delete_manga_entry'),
]