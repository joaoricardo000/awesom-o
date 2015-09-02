from yowsup.layers import YowLayerEvent, YowParallelLayer
from yowsup.layers.auth import YowAuthenticationProtocolLayer, AuthError
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.protocol_messages import YowMessagesProtocolLayer
from yowsup.layers.protocol_media import YowMediaProtocolLayer
from yowsup.layers.protocol_receipts import YowReceiptProtocolLayer
from yowsup.layers.protocol_acks import YowAckProtocolLayer
from yowsup.layers.protocol_iq import YowIqProtocolLayer
from yowsup.layers.axolotl import YowAxolotlLayer
from yowsup.stacks import YowStack, YOWSUP_CORE_LAYERS

from router import RouteLayer


class YowsupEchoStack(object):
    def __init__(self, credentials):
        layers = (RouteLayer,
                  YowParallelLayer([YowAuthenticationProtocolLayer,
                                    YowMessagesProtocolLayer,
                                    YowReceiptProtocolLayer,
                                    YowAckProtocolLayer,
                                    YowMediaProtocolLayer,
                                    YowIqProtocolLayer]),
                  YowAxolotlLayer,
                  ) + YOWSUP_CORE_LAYERS
        self.stack = YowStack(layers)
        self.stack.setCredentials(credentials)

    def start(self):
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        try:
            logging.info("Iniciando server...")
            self.stack.loop()
        except AuthError as e:
            print("Authentication Error: %s" % e.message)


if __name__ == "__main__":
    from config import auth
    import logging

    logging.basicConfig(level=logging.INFO)
    server = YowsupEchoStack(auth)
    while True:
        server.start()