from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from blog.models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'status']


class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ['text']
