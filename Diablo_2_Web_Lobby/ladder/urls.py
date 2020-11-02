from django.urls import path

from . import views

urlpatterns = [
    path('ladder', views.ladderExpStandard, name='ladder'),
    path('ladder/nor/standard', views.ladderNorStandard, name='ladder nor standard'),
    path('ladder/nor/hardcore', views.ladderNorHardcore, name='ladder nor hardcore'),
    path('ladder/exp/standard', views.ladderExpStandard, name='ladder exp standard'),
    path('ladder/exp/hardcore', views.ladderExpHardcore, name='ladder exp hardcore'),
]