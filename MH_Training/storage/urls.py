from django.urls import path

from . import views

urlpatterns = [
    path('storage/', views.storage_main, name='storage_main'),
]