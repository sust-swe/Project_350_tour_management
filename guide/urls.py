# main urls from django.contrib import admin
from django.urls import path, include
from . import views
# main urls from django.conf import settings
# main urls from django.conf.urls.static import static


urlpatterns = [
    path('', views.register, name='aha'),
    path('my_guide/', views.MyGuide.as_view(), name = 'my guide'),
    path('<int:id>/', views.GuideDetail.as_view(), name = 'guide detail'),
    path('<int:id>/update/', views.UpdateGuide.as_view(), name = 'update guide '),
    path('<int:id>/delete/', views.DeleteGuide.as_view(), name = 'delete guide'),
    path('add_guide/', views.AddGuide.as_view(), name = 'add guide'),
]

# urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
