from django.shortcuts import render
from .models import Post
from django.http import HttpResponseRedirect
from .forms import PostForm

# Create your views here.

def blog_list(request):
    posts = Post.objects.all()
    context = {
        'blog_list':posts
    }

    return render(request, "blog/blog_list.html", context)

def blog_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/posts/')
    context = {
        "form":form,
        "form_type":'Create'
    }
    return render(request, "blog/blog_create.html", context)

def blog_update(request, id):
    post = Post.objects.get(id=id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/posts/')
    context = {"form":form,
            "form_type": 'Update'}

    return render(request, "blog/blog_create.html", context)

def blog_detail(request, id):
    each_post = Post.objects.get(id=id)
    context = {
        'blog_detail':each_post
    }

    return render(request, "blog/blog_detail.html", context)

def blog_delete(request, id):
    each_post = Post.objects.get(id=id)
    each_post.delete()
    return HttpResponseRedirect('/posts/')