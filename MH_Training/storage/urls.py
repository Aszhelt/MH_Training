from django.urls import path

from . import views

urlpatterns = [
    path('storage/', views.storage_main, name='storage_main'),
    path('storage/<int:id>/', views.view_item, name='view_item'),
    path('storage/create/', views.create_item, name='create_item'),
]