from django.urls import re_path

from lobby.consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/lobby/(?P<room_name>\w+)/$', ChatConsumer),
]