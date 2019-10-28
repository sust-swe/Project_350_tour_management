from django.db import models
from homepage.models import UserDetail, City
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse
from django.utils.timezone import timezone
# Create your models here.


STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        UserDetail, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return '%s %s' % (self.author.__str__(), self.title)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('bloglist')


class TestP(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.title

# pip install Pillow
# python manage.py makemigrations
# python manage.py sqlmigrate @appname @migrationid
# python manage.py migrate
# django admin username-shoaib password-1234
# python manage.py createsuperuser @username
# python manage.py changepassword @username
# python manage.py createsuperuser -h
