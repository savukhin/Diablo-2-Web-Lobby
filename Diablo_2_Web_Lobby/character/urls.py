from django.urls import path

from . import views

urlpatterns = [
    # path('createCharacter', views.createCharacter, name='create character'),
    path('character/server=<str:server>;name=<str:name>', views.showCharacter, name='character armory'),
    #path('char/<str:name>', views.temp, name='character'),
]