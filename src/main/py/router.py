from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from views import views

import logging
import re
import threading
from views.downloads import ViewsMedia

logger = logging.getLogger(__name__)


class RouteLayer(YowInterfaceLayer):
    def __init__(self):
        super(RouteLayer, self).__init__()

        views_media_download = ViewsMedia(self)
        routes = [("^/piada$", views.get_piada),
                  ("^/eco", views.echo),
                  ("^/ping", views.ping),
                  ] + views_media_download.routes
        self.views = [(re.compile(pattern), callback) for pattern, callback in routes]

    @ProtocolEntityCallback("message")
    def on_message(self, message):
        self.toLower(message.ack(True))
        if message.getType() == 'text':
            threading.Thread(target=self.route, args=(message,)).start()

    def route(self, message):
        text = message.getBody()
        for route, callback in self.views:
            match = route.match(text)
            if match:
                data = callback(message, match)
                if data:
                    self.toLower(data)
                break

    @ProtocolEntityCallback("receipt")
    def on_receipt(self, entity):
        self.toLower(entity.ack())