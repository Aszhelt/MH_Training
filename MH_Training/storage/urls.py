from django.urls import path

from . import views

urlpatterns = [
    path('orders/', views.orders, name="orders"),
    path('orders/<int:id>/', views.view_order, name="view_order"),
    path('item_request/<int:id>/', views.edit_item_request, name="edit_item_request"),
    path('orders/new/', views.new_order, name="new_order"),
    path('storage/', views.storages, name="storages"),
    path('storage/<str:name_storage>/', views.storage_view, name="storage_view"),
]
