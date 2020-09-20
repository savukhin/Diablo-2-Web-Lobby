from django.urls import path

from . import views

urlpatterns = [
    path('createCharacter', views.createCharacter, name='create character'),
]