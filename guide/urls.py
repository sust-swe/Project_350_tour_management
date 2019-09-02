# main urls from django.contrib import admin
from django.urls import path, include
from . import views
# main urls from django.conf import settings
# main urls from django.conf.urls.static import static


urlpatterns = [
    path('', views.register, name='aha')
]

# urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
