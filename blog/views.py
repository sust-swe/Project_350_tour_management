from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from .models import Post, Comment, Preference
from homepage.models import UserDetail
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm, CommentForm, UpdatePostForm
from django import views
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
# Create your views here.
from hitcount.views import HitCountDetailView
from django.core.paginator import Paginator


def blog(request):
    return render(request, 'blog.html')


def new_post(request):
    # post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated:
        user = request.user
        user_detail = UserDetail.objects.get(user=request.user)
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user_detail = user_detail
                instance.save()
                return redirect('/blog/bloglist')
        else:
            form = PostForm()
        return render(request, 'newpost.html', {'form': form})
    else:
        messages.info(request, 'Log in first')
        return redirect('/accounts/login/')


class UpdatePost(views.View):
    template_name = 'update_post.html'
    form_class = PostForm

    def get(self, request, pk):
        if request.user.is_authenticated:
            post = Post.objects.get(pk=pk)
            if post.user_detail.user == request.user:
                form = self.form_class(instance=post)
                return render(request, self.template_name, {'form': form})
            else:
                messages.info(request, 'Permission denied')
                return redirect('/blog/bloglist')
        else:
            messages.info(request, 'Log in First')
            return redirect('/')

    def post(self, request, pk):
        if request.user.is_authenticated:
            instance = Post.objects.get(pk=pk)
            if instance.user_detail.user == request.user:
                form = self.form_class(
                    request.POST, request.FILES, instance=instance)
                if form.is_valid():
                    ob = form.save(commit=False)
                    try:
                        ob.full_clean()
                        ob.save()
                        return redirect('post_detail', pk=instance.pk)
                    except ValidationError as e:
                        nfe = e.message_dict[NON_FIELD_ERRORS]
                        return (request, self.template_name, {'form': form, 'nfe': nfe})
                else:
                    messages.info('Invalid Credentials')
                    return render(request, self.template_name, {'form': form})
            else:
                messages.info(request, 'Permission denied')
                return redirect('post_detail', pk=instance.pk)
        else:
            messages.info(request, 'Log in First')
            return redirect('/')


class DeletePost(views.View):

    def get(self, request, pk):
        if request.user.is_authenticated:
            instance = Post.objects.get(pk=pk)
            if instance.user_detail.user == request.user:
                instance.delete()
                return redirect('/blog/bloglist')
            else:
                messages.info(request, 'Permission denied')
                return redirect('post_detail', pk=instance.pk)
        else:
            messages.info(request, 'You must login first')
            redirect('/')


def PostList(request):
    postlist = Post.objects.filter(status=1).order_by('-created_on')
    paginator = Paginator(postlist, 6)
    # postlistd = Post.objects.filter(status=1).order_by('-created_on')
    page = request.GET.get('page')

    if request.method == 'POST':
        query = request.POST['q']
        print(query)
        if query:
            postlist = Post.objects.filter(
                status=1).filter(title__icontains=query)

    postlist = paginator.get_page(page)

    context = {
        'post_lists': postlist,

    }
    return render(request, 'blogs.html', context)


# class PostDetail(generic.DetailView):
#     model = Post
#     template_name = 'post_detail.html'


class PostDetail(HitCountDetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    count_hit = True

    def get_context_data(self, **kwargs):
        # post = get_object_or_404(Post, pk=pk)
        context = super(PostDetail, self).get_context_data(**kwargs)
        context.update({
            'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],
        }

        )
        # context = {
        #     'post': post,
        #     # 'count_hit': count_hit
        # }
        return context
        # return render(request, 'post_detail.html', context)

    # if request.user.is_authenticated:
    #     user = UserDetail.objects.get(user=request.user)
    #     is_liked = False
    #     if post.likes.filter(pk=request.user.pk).exists():
    #         is_liked = True


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
