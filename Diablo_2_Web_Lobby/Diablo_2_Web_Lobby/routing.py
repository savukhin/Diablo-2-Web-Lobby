from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import lobby.routing
import dialogues.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            lobby.routing.websocket_urlpatterns
            + dialogues.routing.websocket_urlpatterns
        )
    ),
})