from homepage.base import *
from . import views

urlpatterns = [
    # path('login/', login, name='login')
    path('my_residence/', views.MyResidence.as_view(), name='my residence'),
    path('add_residence/', views.AddResidence.as_view(), name='add residence'),
    path('<int:id>/', views.ResidenceDetail.as_view(), name='residence detail'),
    path('<int:id>/update/', views.UpdateResidence.as_view(),
         name='update residence'),
    path('<int:id>/delete/', views.DeleteResidence.as_view(),
         name='delete residence'),
    path('<int:id>/space/', views.ShowResidenceSpace.as_view(), name='show space'),
    path('<int:id>/space/add_space/',
         views.AddSpace.as_view(), name='add residence space'),
    path("<int:id>/space_type/", views.ShowSpaceTypes.as_view()),
    path("<int:residence_id>/create_space_type/",
         views.CreateSpaceType.as_view()),
    path('space/<int:space_id>/', views.SpaceDetail.as_view(), name='Space Detail'),
    path('space/<int:space_id>/update/',
         views.UpdateSpace.as_view(), name='Update Space'),
    path('space/<int:space_id>/delete/',
         views.DeleteSpace.as_view(), name='Delete Space'),
    path('space/<int:space_id>/avail/',
         views.CreateSpaceAvailability.as_view(), name='c_s_a'),
    path("space/<int:space_id>/unavail/", views.MakeSpaceUnavailable.as_view()),
    path("space/<int:space_id>/book/", views.BookSpace.as_view()),
    path("ajax/", include("residence.ajax_handler")),
    path("space_type/<int:space_type_id>/",
         views.ShowSpaceTypeDetail.as_view()),
    path("space_type/<int:space_type_id>/update/",
         views.UpdateSpaceType.as_view()),
    path("space_type/<int:space_type_id>/delete/",
         views.DeleteSpaceType.as_view()),
    path("book/", views.BookSpace.as_view()),
    path("received_order/", views.ShowResidenceOrder.as_view()),
    path("placed_order/", views.ShowPlacedOrder.as_view()),

]
