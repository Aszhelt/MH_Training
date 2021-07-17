from django.urls import path

from . import views

urlpatterns = [
    path('orders/', views.orders, name="orders"),
    path('orders/new/', views.new_order, name="new_order"),
    path('storage/', views.storages, name="storages"),
    path('storage/<str:name_storage>/', views.storage_view, name="storage_view"),
]
