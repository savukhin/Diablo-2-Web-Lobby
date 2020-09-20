from django.urls import path

from . import views

urlpatterns = [
    path('createCharacter', views.createCharacter, name='create character'),
    path('character/<str:name>', views.showCharacter, name='character armory'),
]