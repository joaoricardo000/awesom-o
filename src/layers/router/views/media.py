"""
    Media download request views.

    Handles the media url messages with utilities classes for it.
"""
from utils.media_downloader import ImageSender, VideoSender, YoutubeSender, UrlPrintSender, GoogleTtsSender
import requests


class MediaViews():
    def __init__(self, interface_layer):
        """
            Creates the regex routes and callbacks to handle media messages
        """
        self.image_sender = ImageSender(interface_layer)
        self.video_sender = VideoSender(interface_layer)
        self.yt_sender = YoutubeSender(interface_layer)
        self.url_print_sender = UrlPrintSender(interface_layer)
        self.google_tts_sender = GoogleTtsSender(interface_layer)
        self.routes = [
            ("https?:\/\/(?:[\w\-]+\.)+[a-z]{2,6}(?:\/[^\/#?]+)+\.(?:jpe?g|gif|png)($|\?[^\s]+$)", self.send_image),
            ("https?:\/\/(?:[\w\-]+\.)+[a-z]{2,6}(?:\/[^\/#?]+)+\.(?:mp4|webm)($|\?[^\s]+$)", self.send_video),
            ("https?:\/\/(?:www\.)?youtu(?:be.com\/watch\?v=|\.be/)(?P<video_id>[\w-]+)(&\S*)?$", self.send_yt_video),
            ("https?:\/\/(?:www\.)?[^$]+$", self.send_url_print),
            ("/g(ravar)?\s(?P<text>[^\[]{1,500})\s?\[?(?P<lang>[A-Za-z\-]{2,6})?\]?$", self.send_tts),
            ("/b(uscar)?\s(?P<term>[^$]+)$", self.google_search),
            ("/i(magem)?\s(?P<term>[^$]+)$", self.google_image_search)
        ]

    def send_video(self, message, match):
        self.video_sender.send_by_url(jid=message.getFrom(), file_url=message.getBody())

    def send_yt_video(self, message, match):
        self.yt_sender.send_by_url(jid=message.getFrom(), file_url=match.group("video_id"))

    def send_image(self, message, match):
        self.image_sender.send_by_url(jid=message.getFrom(), file_url=message.getBody())

    def send_url_print(self, message, match):
        self.url_print_sender.send_by_url(jid=message.getFrom(), file_url=message.getBody())

    def send_tts(self, message, match):
        self.google_tts_sender.send(jid=message.getFrom(), text=match.group("text"), lang=match.group("lang"))

    def google_search(self, message, match):
        req = requests.get("http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s" % match.group("term"))
        page_url = req.json()["responseData"]["results"][0]["url"]
        print page_url
        self.url_print_sender.send_by_url(jid=message.getFrom(), file_url=page_url)

    def google_image_search(self, message, match):
        req = requests.get("http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=%s" % match.group("term"))
        image_url = req.json()["responseData"]["results"][0]["url"]
        self.image_sender.send_by_url(jid=message.getFrom(), file_url=image_url)
