import threading
import logging
from layers.web.models import parseGroupListMessage

from layers.web.service.locator import Instance as service_locator
from layers.web.server import app
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_groups.protocolentities.iq_groups_list import ListGroupsIqProtocolEntity
from yowsup.layers.protocol_groups.protocolentities.iq_result_groups_list import ListGroupsResultIqProtocolEntity


class WebLayer(YowInterfaceLayer):
    def __init__(self):
        super(WebLayer, self).__init__()
        self.entity_callbacks = {}
        self.web_thread = None
        service_locator.set_web_layer(self)
        self.db_collection = service_locator.get_db_collection()
        self._start_web_server()

    def _start_web_server(self):
        self.web_thread = threading.Thread(target=app.run)
        self.web_thread.start()

    def _set_callback(self, EntityClass, callback):
        try:
            self.entity_callbacks[EntityClass.__name__].insert(0, callback)
        except:
            self.entity_callbacks[EntityClass.__name__] = [callback, ]

    def _get_callback(self, entity):
        try:
            callback = self.entity_callbacks[entity.__class__.__name__].pop()
        except:
            callback = None
        return callback

    def groups_list_request(self):
        self._set_callback(ListGroupsResultIqProtocolEntity, self.group_list_callback)
        self.toLower(ListGroupsIqProtocolEntity())

    @ProtocolEntityCallback("message")
    def on_message(self, message):
        if message.getType() == 'text' and message.getBody() == "X":
            self.groups_list_request()

    @ProtocolEntityCallback("iq")
    def onIq(self, entity):
        logging.info("WEB!")
        callback = self._get_callback(entity)
        if callback: callback(entity)

    @ProtocolEntityCallback("receipt")
    def on_receipt(self, entity):
        "Auto ack for every message receipt confirmation"
        self.toLower(entity.ack())

    def group_list_callback(self, listGroupsResultIqProtocolEntity):
        groups = parseGroupListMessage(listGroupsResultIqProtocolEntity)
        groups_collection = self.db_collection.groups
        for g in groups:
            groups_collection.update_one({"id": g.id}, {"$set": g.__dict__}, upsert=True)
