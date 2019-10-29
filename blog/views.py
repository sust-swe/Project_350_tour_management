from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from .models import Post, Comment
from homepage.models import UserDetail
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm, CommentForm
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
        user_detail = UserDetail.objects.get(user=user)
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user_detail = user_detail
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


@login_required
def addComment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
