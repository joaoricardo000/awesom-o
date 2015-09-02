from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from resources import piadas
import random


def get_piada(message, match):
    return TextMessageProtocolEntity(piadas.get(), to=message.getFrom())


def echo(message, match):
    return TextMessageProtocolEntity("Eco: %s" % message.getBody().split("/eco", 1)[1], to=message.getFrom())


def ping(message, match):
    if random.randint(0, 10) == 5:
        pong = "Pong caralho!"
    else:
        pong = "Pong!"
    return TextMessageProtocolEntity(pong, to=message.getFrom())