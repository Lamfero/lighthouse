from django.urls import path
from . import views

urlpatterns = [
    path('tariffs', views.tariffs, name="tariffs"),
]