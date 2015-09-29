from layers.web.service.locator import Instance as service_locator
import web


class hello:
    def GET(self, name):
        service_locator.web_layer.groups_list_request()
        if not name:
            name = 'World'
        return 'Hello, ' + name + '!'


urls = (
    '/(.*)', 'hello'
)

import signal
import sys


def signal_handler(signal, frame):
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
app = web.application(urls, globals())
