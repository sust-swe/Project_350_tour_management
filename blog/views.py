from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from .models import Post
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm
from django import views
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
# Create your views here.


def blog(request):
    return render(request, 'blog.html')


def new_post(request):
    # post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated:
        user = request.user
        user_detail = UserDetail.objects.get(user=request.user)
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = user_detail
                instance.save()
                return redirect('bloglist')
        else:
            form = PostForm()
        return render(request, 'newpost.html', {'form': form})
    else:
        messages.info(request, 'Log in first')
        return redirect('/login/')

def PostList(request):
    postlist = Post.objects.filter(status=1).order_by('-created_on')
    context = {
        'post_lists': postlist
    }
    return render(request, 'blogs.html', context)


# class PostDetail(generic.DetailView):
#     model = Post
#     template_name = 'post_detail.html'


def PostDetail(request, pk):
    detail = get_object_or_404(Post, pk=pk)

    context = {
        'detail': detail
    }
    return render(request, 'post_detail.html', context)