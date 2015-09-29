# coding=utf-8
from utils.media_downloader import ImageSender, VideoSender, YoutubeSender, UrlPrintSender, GoogleTtsSender, AudioSender
from yowsup.layers.protocol_messages.protocolentities.message_text import TextMessageProtocolEntity
import random
import sys, os


class StaticViews():
    def __init__(self, interface_layer):
        """
            Creates the regex routes and callbacks to handle media messages
        """
        self.interface_layer = interface_layer
        self.google_tts_sender = GoogleTtsSender(self.interface_layer)
        self.url_print_sender = UrlPrintSender(self.interface_layer)
        self.audio_sender = AudioSender(self.interface_layer)
        self.resource_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../resources/")
        self.routes = [
            # ("^/oi", self.oi),
            ("^/folha", self.folha),
            ("^/ajuda", self.ajuda),
            ("^/g1", self.g1),
            ("^/ge", self.ge),
            ("^/rola", self.rola),
            ("^/gira", self.gira),
            ("^/s(erie)?(?P<serie>[abcd])\s*$", self.brasileirao),
            ("^/(?P<im>im)?par\s*$", self.par),
        ]

    def oi(self, message=None, match=None, to=None):
        to = to or message.getFrom()
        welcome_text = """
Oi! Eu sou a claudinete, Com dois dês e Ípsilon
Claudi, para os íntimos.

Eu sou uma assistente pessoal de whatsapp.
Para ver como posso te ajudar, me envie barra ajuda.
Beijos no coração.
            """
        self.google_tts_sender.send(to, welcome_text)
        welcome_text = """
Oi! Eu sou a Clauddy.net, com dois 'd's e 'y'.
Clauddy, para os íntimos.
Eu sou uma assistente pessoal de whatsapp.
Para ver como posso te ajudar, me envie:
/ajuda

Beijos no coração.
        """
        self.interface_layer.toLower(TextMessageProtocolEntity(to=to, body=welcome_text))

    def ajuda(self, message=None, match=None, to=None):
        ajuda_text = """ [Ajuda]
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
        return TextMessageProtocolEntity(ajuda_text, to=message.getFrom())

    def g1(self, message=None, match=None, to=None):
        to = to or message.getFrom()
        self.url_print_sender.send_by_url(to, "http://g1.globo.com/")

    def rola(self, message=None, match=None, to=None):
        return TextMessageProtocolEntity("[%d]" % random.randint(1, 6), to=message.getFrom())

    def gira(self, message=None, match=None, to=None):
        to = to or message.getFrom()
        self.audio_sender.send_file_by_path(to, self.resource_path + "audio/piao.mp3")
        return TextMessageProtocolEntity("Giraaandooo... [%d]" % random.randint(1, 6), to=to)

    def par(self, message=None, match=None, to=None):
        impar = match.group("im")
        num = random.randint(1, 10)
        if (impar and not num % 2) or (not impar and num % 2):
            return TextMessageProtocolEntity("[%d]\nERRROOOOOOOUU!" % num, to=message.getFrom())
        else:
            return TextMessageProtocolEntity("[%d]\nuau, parabéns..." % num, to=message.getFrom())

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
