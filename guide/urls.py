# main urls from django.contrib import admin
from django.urls import path, include
from . import views
# main urls from django.conf import settings
# main urls from django.conf.urls.static import static


urlpatterns = [
    path('', views.register, name='aha'),
    path('my_guide/', views.MyGuide.as_view(), name='my guide'),
    path('<int:id>/', views.GuideDetail.as_view(), name='guide detail'),
    path('<int:id>/update/', views.UpdateGuide.as_view(), name='update guide '),
    path('<int:id>/delete/', views.DeleteGuide.as_view(), name='delete guide'),
    path("<int:guide_id>/availability/", views.GuideAvailability.as_view()),
    path('add_guide/', views.AddGuide.as_view(), name='add guide'),
    path("<int:guide_id>/avail/", views.CreateGuideAvailability.as_view()),
    path("<int:guide_id>/unavail/", views.MakeGuideUnavailable.as_view()),
    path("<int:guide_id>/bookings/", views.GuideBookings.as_view()),
    path("book/", views.BookGuide.as_view()),
    path("purchased_order/", views.ShowPurchasedOrder.as_view()),
    path("bookings/<int:booking_id>/", views.ShowGuideBookingDetail.as_view())
]

# urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
