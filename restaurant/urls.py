# main urls from django.contrib import admin
from django.urls import path, include
from . import views
# main urls from django.conf import settings
# main urls from django.conf.urls.static import static


urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', include('homepage.urls')),
    # path('login/', views.login, name='login')
    path('myrestaurant/', views.my_restaurant, name='my restaurant'),
    path('addres/', views.add_restaurant, name='add restaurants'),
]

# urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
