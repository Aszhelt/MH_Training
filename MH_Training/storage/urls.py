from django.urls import path

from . import views

urlpatterns = [
    path('event/', views.events, name="events"),
    path('event/create/', views.create_event, name="create_event"),
    path('event/<int:id>/', views.view_event, name="view_event"),
    path('item_request/create/', views.create_item_request, name="create_item_request"),
    path('item_request/<int:id>/', views.view_item_request, name="view_item_request"),
]
