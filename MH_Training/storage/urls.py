from django.urls import path

from . import views

urlpatterns = [
    path('storage/', views.storage_main, name='storage_main'),
    path('<int:id>/', views.view_item, name='view_item'),
    path('<str:name>/', views.view_group, name='view_group'),
    path('create/', views.create_item, name='create_item'),
]