from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
import random


def echo(message, match):
    return TextMessageProtocolEntity("Eco: %s" % match.group("echo_message"), to=message.getFrom())


def ping(message, match):
    if random.randint(0, 10) == 5:
        pong = "Pong caralho!"
    else:
        pong = "Pong!"
    return TextMessageProtocolEntity(pong, to=message.getFrom())
