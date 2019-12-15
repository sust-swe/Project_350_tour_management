from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from blog.models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'status', 'display_pic']
        labels = {
            'title': 'Title',
            'content': 'Post Description',
            'display_pic': 'Display Photo'

        }


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'status', 'display_pic']
        labels = {
            'title': 'Title',
            'content': 'Post Description',

        }


class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ['text']
        labels = {
            'text': ''
        }

        # widgets = {
        #     # The class here is a CSS class.
        #     # 'title' : forms.TextInput(attrs={'class':'TextInputClass'}), #TextInputClass is our class
        #     # postcontent class is our class
        #     'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        # }
