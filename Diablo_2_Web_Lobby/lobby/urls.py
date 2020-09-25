from django.urls import path

from . import views

urlpatterns = [
    path('lobby', views.prelobby, name='preLobby'),
    path('lobby/char=<str:name>', views.lobby, name='lobby'),
    path('create_game/char=<str:name>', views.createGame, name='createGame'),
]