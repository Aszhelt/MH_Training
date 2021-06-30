from django.urls import path

from . import views

urlpatterns = [
    path('storage/', views.storage_main, name='storage_main'),
    path('storage/<int:id>/', views.view_item, name='view_item'),
    path('storage/<str:item_group_name>/', views.view_group, name='view_group'),
]