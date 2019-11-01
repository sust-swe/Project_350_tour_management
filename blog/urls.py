from django.urls import path, include
from . import views
from django.conf.urls import url, include

urlpatterns = [
    path('', views.blog, name='blog'),
    # path('', views.new_post.as_view(), name='newpost'),
    path('newpost/', views.new_post, name='newpost'),
    # url(r'^newpost(?P<pk>[0-9]+)/$', views.new_post, name='newpost'),
    path('bloglist/', views.PostList, name='bloglist'),
    # path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    url(r'^(?P<pk>[0-9]+)/$', views.PostDetail, name='post_detail'),
    url(r'^(?P<pk>[0-9]+)/comment/$', views.addComment, name='addcomment'),
    url(r'^comment/(?P<pk>[0-9]+)/approve/$',
        views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>[0-9]+)/remove/$',
        views.comment_remove, name='comment_remove'),
    
]
