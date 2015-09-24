"""
    The Route Layer.
    Here the message is routed to its proper view.
    The routes are defined with regular expressions and callback functions (just like any web framework).
"""

from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback

from views import views
from views.media import MediaViews
from views.group_admin import GroupAdminViews

import threading
import re
import logging


class RouteLayer(YowInterfaceLayer):
    def __init__(self):
        """
            The definition of routes and views (callbacks)!

            For the simple message handling, just calls the callback function, and expects a message entity to return.
            For more complex handling, like asynchronous file upload and sending, it creates a object passing 'self',
            so the callback can access the 'self.toLower' method
        """
        super(RouteLayer, self).__init__()

        routes = [("^/ping", views.ping),
                  ("^/eco(?P<eco_message>[^$]+)$", views.echo),
                  ("^/piada\s*$", views.get_piada)]

        routes.extend(MediaViews(self).routes)
        # routes.extend(GroupAdminViews(self).routes)

        self.views = [(re.compile(pattern), callback) for pattern, callback in routes]

    def route(self, message):
        "Get the text from message and tests on every route for a match"
        text = message.getBody()
        for route, callback in self.views:
            match = route.match(text)
            if match:  # in case of regex match, the callback is called, passing the message and the match object
                threading.Thread(target=self.handle_callback, args=(callback, message, match)).start()
                break

    def handle_callback(self, callback, message, match):
        logging.info("Threads: %s" % threading.active_count())
        try:
            logging.info("[%s][%s]\t%s" % (message.getParticipant(), message.getFrom(), message.getBody()))
            data = callback(message, match)
            if data: self.toLower(data)  # if callback returns a message entity, sends it.
        except Exception as e:
            logging.exception("Erro no roteamento da mensagem %s" % message)

    @ProtocolEntityCallback("message")
    def on_message(self, message):
        "Executes on every received message"
        self.toLower(message.ack())  # Auto ack (double blue check symbol)
        self.toLower(message.ack(True))  # Auto ack (double blue check symbol)
        # Routing only text type messages, for now ignoring other types. (media, audio, location...)
        if message.getType() == 'text':
            # Route the message on a new thread to not block the others messages (probably needs performance enhance)
            self.route(message)

    @ProtocolEntityCallback("receipt")
    def on_receipt(self, entity):
        "Auto ack for every message receipt confirmation"
        self.toLower(entity.ack())
