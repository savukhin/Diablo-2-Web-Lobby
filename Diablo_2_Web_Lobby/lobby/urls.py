from django.urls import path

from . import views

urlpatterns = [
    path('lobby', views.lobby, name='lobby'),
    path('create_game', views.createGame, name='createGame'),
]