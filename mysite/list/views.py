from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests

from .models import MangaReadingList
from .forms import CustomUserCreationForm, LoginForm, MangaListUpdateForm

CLIENT_ID = 'bf6b2a5a88869a2996582f2d37f1c6cb'

def home_view(request):
    return render(request, 'base.html')

def fetch_manga_list(request):
    url = "https://api.myanimelist.net/v2/manga/ranking"
    headers = {"X-MAL-CLIENT-ID": CLIENT_ID}

    page = max(int(request.GET.get('page', 1)), 1)
    query = request.GET.get('query', '').strip()
    limit = 50
    offset = (page - 1) * limit

    params = {
        "ranking_type": "all",
        "limit": limit,
        "offset": offset,
        "fields": "title,alternative_titles,num_chapters,num_volumes,rank,main_picture,status,synopsis,genres",
    }

    try:
        # Default ranking or search logic
        if not query:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            mangas = data.get('data', [])
            
            # Use next/previous links to determine pagination
            paging = data.get('paging', {})
            has_next = 'next' in paging
            has_previous = 'previous' in paging
            
            # Estimate total pages based on offset and has_next
            total_pages = page + (1 if has_next else 0)
        else:
            # Search scenario
            url = "https://api.myanimelist.net/v2/manga"
            params["q"] = query
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            mangas = data.get('data', [])
            
            paging = data.get('paging', {})
            has_next = 'next' in paging
            has_previous = 'previous' in paging
            total_pages = page + (1 if has_next else 0)

    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        mangas = []
        has_next = False
        has_previous = False
        total_pages = 1

    # Intelligent page range generation
    page_range = []
    if total_pages <= 5:
        page_range = list(range(1, total_pages + 1))
    else:
        if page <= 3:
            page_range = list(range(1, min(6, total_pages + 1)))
        elif page >= total_pages - 2:
            page_range = list(range(max(1, total_pages - 4), total_pages + 1))
        else:
            page_range = list(range(page - 2, page + 3))

    context = {
        'mangas': mangas,
        'current_page': page,
        'has_next': has_next,
        'has_previous': has_previous,
        'pages': page_range,
        'total_pages': total_pages,
        'query': query
    }

    return render(request, 'list/manga_list.html', context)

def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('manga_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('manga_list')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('manga_list')
@login_required
def add_to_list(request):
    if request.method == 'GET':
        manga_id = request.GET.get('manga_id')
        
        # Fetch manga details from MyAnimeList API
        url = f"https://api.myanimelist.net/v2/manga/{manga_id}"
        headers = {"X-MAL-CLIENT-ID": CLIENT_ID}
        params = {"fields": "title,main_picture,num_chapters,num_volumes"}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            # Correctly define manga_data here
            manga_data = response.json()
            
            # Check if manga already exists in user's list
            existing_entry = MangaReadingList.objects.filter(
                user=request.user, 
                manga_id=manga_id
            ).first()
            
            if existing_entry:
                messages.warning(request, 'Manga is already in your list!')
                return redirect('manga_list')
            
            # Create new list entry
            manga_list_entry = MangaReadingList.objects.create(
                user=request.user,
                manga_id=manga_id,
                manga_title=manga_data.get('title', 'Unknown Title'),
                manga_image_url=manga_data.get('main_picture', {}).get('medium'),
                reading_status='plan_to_read',
                num_chapters_read=0,
                num_volumes_read=0
            )
            
            messages.success(request, f'Added "{manga_list_entry.manga_title}" to your list!')
            return redirect('my_manga_list')
        
        except requests.exceptions.RequestException as e:
            messages.error(request, f'Error fetching manga details: {str(e)}')
            return redirect('manga_list')

@login_required
def my_manga_list(request):
    reading_lists = MangaReadingList.objects.filter(user=request.user)
    
    # Optional: Filter by reading status
    status_filter = request.GET.get('status', '')
    if status_filter:
        reading_lists = reading_lists.filter(reading_status=status_filter)
    
    context = {
        'reading_lists': reading_lists,
        'statuses': dict(MangaReadingList.STATUS_CHOICES)
    }
    # Print the current user
    print(f"Current User: {request.user}")

    # Get reading lists
    reading_lists = MangaReadingList.objects.filter(user=request.user)
    
    # Print the number of entries
    print(f"Number of Manga Entries: {reading_lists.count()}")

    return render(request, 'list/my_manga_list.html', context)

@login_required
def update_manga_list_entry(request, entry_id):
    entry = MangaReadingList.objects.get(id=entry_id, user=request.user)
    
    if request.method == 'POST':
        form = MangaListUpdateForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Manga entry updated successfully!')
            return redirect('my_manga_list')
    else:
        form = MangaListUpdateForm(instance=entry)
    
    return render(request, 'list/update_manga_entry.html', {'form': form, 'entry': entry})

@login_required
def delete_manga_list_entry(request, entry_id):
    try:
        entry = MangaReadingList.objects.get(id=entry_id, user=request.user)
        entry.delete()
        messages.success(request, f'Successfully removed "{entry.manga_title}" from your list.')
    except MangaReadingList.DoesNotExist:
        messages.error(request, 'Manga entry not found.')
    
    return redirect('my_manga_list')