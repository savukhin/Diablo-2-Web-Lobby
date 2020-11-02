from django.urls import re_path

from dialogues.consumer import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/dialogue/(?P<room_name>\w+)/$', ChatConsumer),
]