# -*- coding: utf-8 -*-

from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from channels.sessions import SessionMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
import startup_view.routing

MiddlewareStack = lambda inner:AllowedHostsOriginValidator(
        SessionMiddlewareStack(inner)
    )

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': SessionMiddlewareStack(
        URLRouter(
            startup_view.routing.websocket_urlpatterns
        )
    ),
    'channel': ChannelNameRouter({
        "scripthandler": startup_view.routing.worker_channelname,
    })
})

