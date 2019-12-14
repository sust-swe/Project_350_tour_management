from django.db import models
from homepage.models import UserDetail, City
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse

from django.utils.timezone import timezone
from django.db import IntegrityError
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.


STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=200)
    user_detail = models.ForeignKey(
        UserDetail, on_delete=models.CASCADE)
    display_pic = models.ImageField(upload_to='blog_pics',
                                    null=True, blank=True, default=None)
    updated_on = models.DateTimeField(auto_now=True)
    content = RichTextUploadingField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')

    class Meta:
        ordering = ['-created_on']

    def approve_comments(self):
        return self.comments.filter(approve_comment=True)
        # return self.comments.filter(approve_comment=True)

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return '%s %s' % (self.user_detail.__str__(), self.title)


class Preference(models.Model):
    user_detail = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user_detail) + ':' + str(self.post) + ':' + str(self.value)

    class Meta:
        unique_together = ("user_detail", "post", "value")


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    user_detail = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    text = RichTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approve_comment = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    def approve(self):
        self.approve_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('bloglist', kwargs={'pk': self.pk})


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
