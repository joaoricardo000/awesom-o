import random
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from layers.router.resources import piadas


def get_piada(message, match):
    return TextMessageProtocolEntity(piadas.get(), to=message.getFrom())


def echo(message, match):
    return TextMessageProtocolEntity("Eco: %s" % match.group("eco_message"), to=message.getFrom())


def ping(message, match):
    if random.randint(0, 10) == 5:
        pong = "Pong caralho!"
    else:
        pong = "Pong!"
    return TextMessageProtocolEntity(pong, to=message.getFrom())
