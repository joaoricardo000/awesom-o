# coding=utf-8
from utils.media_sender import UrlPrintSender, GoogleTtsSender, AudioSender
from yowsup.layers.protocol_messages.protocolentities.message_text import TextMessageProtocolEntity
import random
import os
import emoji
import shelve
from views.resources import piadas

emoticon_lose = emoji.emojize(":x:", True).encode("UTF-8")
emoticon_notlose = emoji.emojize(":o:", True).encode("UTF-8")


class AwesomoViews():
    def __init__(self, interface_layer):
        """
            Creates the regex routes and callbacks to handle media messages
        """
        self.interface_layer = interface_layer
        self.google_tts_sender = GoogleTtsSender(self.interface_layer)
        self.url_print_sender = UrlPrintSender(self.interface_layer)
        self.audio_sender = AudioSender(self.interface_layer)
        self.resource_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./resources/")
        self.routes = [
            ("^/folha", self.folha),
            ("^/ajuda", self.ajuda),
            ("^/g1", self.g1),
            ("^/ge", self.ge),
            ("^/rola", self.rola),
            ("^/gira", self.gira),
            ("^/s(erie)?(?P<serie>[abcd])\s*$", self.brasileirao),
            ("^/p(iada)?$", self.piada),
            ("^/(?P<im>im)?par\s*$", self.par),
        ]
        self.collection_losers = shelve.open("losers.data")

    def ajuda(self, message=None, match=None, to=None):
        return TextMessageProtocolEntity(HELP_TEXT, to=message.getFrom())

    def rola(self, message=None, match=None, to=None):
        return TextMessageProtocolEntity("[%d]" % random.randint(1, 6), to=message.getFrom())

    def gira(self, message=None, match=None, to=None):
        to = to or message.getFrom()
        self.audio_sender.send_by_path(to, self.resource_path + "audio/piao.mp3")
        return TextMessageProtocolEntity("Giraaandooo... [%d]" % random.randint(1, 6), to=to)

    def piada(self, message, match):
        return TextMessageProtocolEntity(piadas.get(), to=message.getFrom())

    def par(self, message=None, match=None, to=None):
        is_odd = bool(match.group("im"))
        num = random.randint(1, 10)
        lost = (is_odd and num % 2) or (not is_odd and not num % 2)
        score = self._save_game(message.getFrom(), lost)
        response = "[%d] Você %s\n\n%s\n%s" % (num,
                                               "ganhou." if lost else "perdeu!",
                                               emoticon_lose * score[0],
                                               emoticon_notlose * score[1])
        return TextMessageProtocolEntity(response, to=message.getFrom())

    def _save_game(self, loser, lose=True):
        losing_history = self.collection_losers.get(loser, {True: 0, False: 0})
        losing_history[lose] += 1
        self.collection_losers[loser] = losing_history
        self.collection_losers.sync()
        return losing_history

    def g1(self, message=None, match=None, to=None):
        to = to or message.getFrom()
        self.url_print_sender.send_by_url(to, "http://g1.globo.com/")

    def folha(self, message=None, match=None, to=None):
        to = to or message.getFrom()
        self.url_print_sender.send_by_url(to, "http://www.folha.uol.com.br/")

    def ge(self, message=None, match=None, to=None):
        to = to or message.getFrom()
        self.url_print_sender.send_by_url(to, "http://globoesporte.globo.com/")

    def brasileirao(self, message=None, match=None, to=None):
        to = to or message.getFrom()
        serie = match.group("serie")
        self.url_print_sender.send_by_url(to, "http://globoesporte.globo.com/futebol/brasileirao-serie-%s/" % serie)


HELP_TEXT = """ [Ajuda]
- Comandos
/ajuda - Mostra esse texto
/b(usca) - Busca do Google
/gira - Girar o peão
/g(ravar) - Gravar um texto
/i(magem) - Busca de imagem do Google
/(im)par - Jogo de par ou impar
/p(iada) - Piada!
/ping - Pong
/s(erie)[a-d] - Tabela do Brasileirao

- Jornais:
/g1
/folha

- Download de urls do YouTube, imagens e videos.
- Print screen de urls
"""
