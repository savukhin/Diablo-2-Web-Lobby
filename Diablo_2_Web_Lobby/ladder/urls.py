from django.urls import path

from . import views

urlpatterns = [
    path('ladder', views.ladder, name='ladder'),
    path('ladder/nor/standard/<str:server>', views.ladderNorStandard, name='ladder nor standard'),
    path('ladder/nor/hardcore/<str:server>', views.ladderNorHardcore, name='ladder nor hardcore'),
    path('ladder/exp/standard/<str:server>', views.ladderExpStandard, name='ladder exp standard'),
    path('ladder/exp/hardcore/<str:server>', views.ladderExpHardcore, name='ladder exp hardcore'),
]