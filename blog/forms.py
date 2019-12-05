from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from blog.models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'status', 'display_pic']

        widgets = {
            # The class here is a CSS class.
            'title' : forms.TextInput(attrs={
                'class':'form-control posttitletext',
                'placeholder':'Enter Title',
            }), #TextInputClass is our class
            # postcontent class is our class
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':'Post Description',
                }),
        }


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'status', 'display_pic']


class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ['text']

        # widgets = {
        #     # The class here is a CSS class.
        #     # 'title' : forms.TextInput(attrs={'class':'TextInputClass'}), #TextInputClass is our class
        #     # postcontent class is our class
        #     'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        # }
