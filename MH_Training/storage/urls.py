from django.urls import path

from . import views

urlpatterns = [
    path('orders/', views.orders, name="orders"),
    path('orders/new/', views.new_order, name="new_order"),
]
