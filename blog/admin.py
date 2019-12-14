from django.contrib import admin
from blog.models import Post, Comment, Preference
# Register your models here.


class PostAdmin(admin.ModelAdmin):

    search_fields = ['title']


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Preference)
