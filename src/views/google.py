"""
    GoogleViews:
    /s(earch) <term>
    youtube urls

"""
from utils.media_sender import YoutubeSender, UrlPrintSender
import requests, urllib


class GoogleViews():
    def __init__(self, interface_layer):
        self.yt_sender = YoutubeSender(interface_layer)
        self.url_print_sender = UrlPrintSender(interface_layer)
        self.routes = [
            (".*https?:\/\/(?:www\.|m\.)?youtu(?:be.com\/watch\?v=|\.be/)(?P<video_id>[\w-]+)(&\S*)?$",
             self.send_yt_video),
            ("/b(usca)?\s(?P<term>[^$]+)$", self.google_search),
        ]

    def send_yt_video(self, message, match):
        self.yt_sender.send_by_url(jid=message.getFrom(), file_url=match.group("video_id"))

    def google_search(self, message, match):
        req = requests.get("http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s" % match.group("term"))
        page_url = urllib.unquote(req.json()["responseData"]["results"][0]["url"])
        self.url_print_sender.send_by_url(jid=message.getFrom(), file_url=page_url)