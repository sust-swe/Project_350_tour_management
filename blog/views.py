from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from .models import Post, Comment, Preference
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
        user_detail = UserDetail.objects.get(user=request.user)
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user_detail = user_detail
                instance.save()
                return redirect('/blog/bloglist/')
        else:
            form = PostForm()
        return render(request, 'newpost.html', {'form': form})
    else:
        messages.info(request, 'Log in first')
        return redirect('/accounts/login/')


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
    post = get_object_or_404(Post, pk=pk)
    # if request.user.is_authenticated:
    #     user = UserDetail.objects.get(user=request.user)
    #     is_liked = False
    #     if post.likes.filter(pk=request.user.pk).exists():
    #         is_liked = True

    context = {
        'post': post,
        # 'is_liked': is_liked,
        # 'total_likes': post.total_likes(),
    }
    return render(request, 'post_detail.html', context)


@login_required
def PostPreference(request, postid, userpreference):

    if request.method == "POST":
        post = get_object_or_404(Post, id=postid)

        obj = ''

        valueobj = ''

        user = request.user
        user_detail = UserDetail.objects.get(user=request.user)

        try:
            obj = Preference.objects.get(user_detail=user_detail, post=post)

            valueobj = obj.value  # value of userpreference

            valueobj = int(valueobj)

            userpreference = int(userpreference)

            if valueobj != userpreference:
                obj.delete()

                upref = Preference()
                upref.user_detail = user_detail

                upref.post = post

                upref.value = userpreference

                if userpreference == 1 and valueobj != 1:
                    post.likes += 1
                    post.dislikes -= 1
                elif userpreference == 2 and valueobj != 2:
                    post.dislikes += 1
                    post.likes -= 1

                upref.save()

                post.save()

                context = {'post': post,
                           'postid': postid}

                return render(request, 'post_detail.html', context)

            elif valueobj == userpreference:
                obj.delete()

                if userpreference == 1:
                    post.likes -= 1
                elif userpreference == 2:
                    post.dislikes -= 1

                post.save()

                context = {'post': post,
                           'postid': postid}

                return render(request, 'post_detail.html', context)

        except Preference.DoesNotExist:
            upref = Preference()

            upref.user_detail = user_detail

            upref.post = post

            upref.value = userpreference

            userpreference = int(userpreference)

            if userpreference == 1:
                post.likes += 1
            elif userpreference == 2:
                post.dislikes += 1

            upref.save()

            post.save()

            context = {'post': post,
                       'postid': postid}

            return render(request, 'post_detail.html', context)

    else:
        post = get_object_or_404(Post, id=postid)
        context = {'post': post,
                   'postid': postid}

        return render(request, 'post_detail.html', context)

# def like_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.user.is_authenticated:
#         user = UserDetail.objects.get(user=request.user)
#         is_liked = False
#         if post.likes.filter(pk=request.user.pk).exists():
#             post.likes.remove(request.user)
#             is_liked = False
#         else:
#             post.likes.add(request.user)
#             is_liked = True

#     # post.likes.add(request.user)
#     return HttpResponseRedirect(post.get_absolute_url())


@login_required
def addComment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    user_detail = UserDetail.objects.get(user=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user_detail = user_detail
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


# class PostUpdateView(LoginRequiredMixin, UpdateView):
#     # if this person is not logged in, where should this person go? To login_url
#     login_url = '/login/'
#     redirect_field_name = 'post_detail.html'
#     form_class = PostForm
#     model = Post


# class PostDeleteView(LoginRequiredMixin, DeleteView):
#     model = Post
#     success_url = reverse_lazy('post_list')
