from yowsup.layers.protocol_media.mediauploader import MediaUploader
from yowsup.layers.protocol_media.protocolentities.iq_requestupload import RequestUploadIqProtocolEntity
from yowsup.layers.protocol_media.protocolentities.message_media_downloadable import \
    DownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_media.protocolentities.message_media_downloadable_image import \
    ImageDownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_media.protocolentities.message_media_downloadable_video import \
    VideoDownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity

import sys
import os
import logging
import requests
import shutil
import hashlib
import re
import config
from pytube import YouTube

logger = logging.getLogger(__name__)


class MediaSender():
    def __init__(self, interface_layer, storage_path=config.media_storage_path):
        self.interface_layer = interface_layer
        self.storage_path = storage_path
        self.file_extension_regex = re.compile("\.([0-9a-z]+)($|\?[^\s]*$)")
        self.MEDIA_TYPE = None

    def send_by_url(self, jid, file_url):
        try:
            self.interface_layer.toLower(TextMessageProtocolEntity("{ baixando [%s]... }" % self.MEDIA_TYPE, to=jid))
            file_path = self._download_file(file_url)
            self.send_file_by_path(jid, file_path)
        except Exception as e:
            logging.exception(e)
            self._on_error(jid)

    def send_file_by_path(self, jid, path):
        entity = RequestUploadIqProtocolEntity(self.MEDIA_TYPE, filePath=path)
        success_callback = lambda successEntity, originalEntity: self._on_upload_result(jid, path, successEntity,
                                                                                        originalEntity)
        err_callback = lambda errorEntity, originalEntity: self._on_error(jid)
        self.interface_layer._sendIq(entity, success_callback, err_callback)

    def _download_file(self, file_url):
        file_path = self._build_file_path(file_url)
        if not os.path.isfile(file_path):
            response = requests.get(file_url, stream=True)
            with open(file_path, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
        return file_path

    def _on_upload_result(self, jid, file_path, upload_result, requestUploadIqProtocolEntity):
        if upload_result.isDuplicate():
            self._doSendFile(file_path, upload_result.getUrl(), jid, upload_result.getIp())
        else:
            callback = lambda file_path, jid, url: self._doSendFile(file_path, url, jid, upload_result.getIp())
            mediaUploader = MediaUploader(jid, self.interface_layer.getOwnJid(), file_path,
                                          upload_result.getUrl(),
                                          upload_result.getResumeOffset(),
                                          callback, self._on_error, self._on_upload_progress, async=True)
            mediaUploader.start()

    def _doSendFile(self, file_path, url, to, ip=None, caption=None):
        entity = None
        if self.MEDIA_TYPE == DownloadableMediaMessageProtocolEntity.MEDIA_TYPE_VIDEO:
            entity = VideoDownloadableMediaMessageProtocolEntity.fromFilePath(file_path, url, self.MEDIA_TYPE, ip, to)
        elif self.MEDIA_TYPE == DownloadableMediaMessageProtocolEntity.MEDIA_TYPE_IMAGE:
            entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(file_path, url, ip, to, caption=caption)
        self.interface_layer.toLower(entity)

    def _on_upload_progress(self, filePath, jid, url, progress):
        if progress % 25 == 0:
            logging.info("[Upload progress]%s => %s, %d%% \r" % (os.path.basename(filePath), jid, progress))

    def _on_error(self, jid, *args, **kwargs):
        error_message = "{! foi mal, deu erro com [%s]... }" % self.MEDIA_TYPE
        self.interface_layer.toLower(TextMessageProtocolEntity(error_message, to=jid))

    def _get_file_ext(self, url):
        return self.file_extension_regex.findall(url)[0][0]

    def _build_file_path(self, url):
        id = hashlib.md5(url).hexdigest()
        return ''.join([self.storage_path, id, ".", self._get_file_ext(url)])


class VideoSender(MediaSender):
    def __init__(self, interface_layer):
        MediaSender.__init__(self, interface_layer)
        self.MEDIA_TYPE = RequestUploadIqProtocolEntity.MEDIA_TYPE_VIDEO


class ImageSender(MediaSender):
    def __init__(self, interface_layer):
        MediaSender.__init__(self, interface_layer)
        self.MEDIA_TYPE = RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE


class YoutubeSender(VideoSender):
    def _download_file(self, video_id):
        file_path = self._build_file_path(video_id)
        if not os.path.isfile(file_path):
            yt = YouTube()
            yt.from_url("http://youtube.com/watch?v=" + video_id)
            video = yt.filter('mp4')[0]
            logging.info(video)
            logging.info(file_path)
            video.download(file_path)
        return file_path

    def _build_file_path(self, video_id):
        return ''.join([self.storage_path, video_id, ".mp4"])
