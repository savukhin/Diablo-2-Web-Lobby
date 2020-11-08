from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('serverInfo/<str:server>', views.serverInfo, name='serverInfo'),
]