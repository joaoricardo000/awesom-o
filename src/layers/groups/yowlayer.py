# coding=utf-8
import config
from layers.router.views.static import StaticViews
from utils.media_downloader import GoogleTtsSender
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_groups.protocolentities.iq_groups_leave import LeaveGroupsIqProtocolEntity
from yowsup.layers.protocol_groups.protocolentities.iq_result_groups_list import ListGroupsResultIqProtocolEntity
from yowsup.layers.protocol_groups.protocolentities.notification_groups_add import AddGroupsNotificationProtocolEntity
from yowsup.layers.protocol_groups.protocolentities.notification_groups_create import \
    CreateGroupsNotificationProtocolEntity
from yowsup.layers.protocol_groups.protocolentities.notification_groups_remove import \
    RemoveGroupsNotificationProtocolEntity
from yowsup.layers.protocol_messages.protocolentities.message_text import TextMessageProtocolEntity


class GroupLayer(YowInterfaceLayer):
    def __init__(self):
        super(GroupLayer, self).__init__()

    @ProtocolEntityCallback("notification")
    def onNotification(self, notification):
        self.toLower(notification.ack())
        if isinstance(notification, CreateGroupsNotificationProtocolEntity):  # added on new group
            self.on_created_group(notification)
        elif isinstance(notification, ListGroupsResultIqProtocolEntity):
            self.on_groups_list(notification)
        # elif isinstance(notification, RemoveGroupsNotificationProtocolEntity):
        #     pass
        # elif isinstance(notification, AddGroupsNotificationProtocolEntity):
        #     pass

    def on_groups_list(self, listGroupResultEntity):
        groups = listGroupResultEntity.getGroups()
        for g in groups:
            if not self.is_allowed_on_group(g):
                self.leave_group(g)

    def is_allowed_on_group(self, group_entity):
        isAllowed = False
        for jid, isAdmin in group_entity.getParticipants().iteritems():
            if jid in config.admins:
                isAllowed = True
                break
        return isAllowed

    def on_created_group(self, createGroupsNotificationProtocolEntity):
        group_id = createGroupsNotificationProtocolEntity.getGroupId() + "@g.us"
        if self.is_allowed_on_group(createGroupsNotificationProtocolEntity):
            pass
            # StaticViews(self).oi(to=group_id)
        else:
            self.toLower(LeaveGroupsIqProtocolEntity(group_id))

    def leave_group(self, group_entity):
        group_id = group_entity.getGroupId() + "@g.us"
        self.toLower(LeaveGroupsIqProtocolEntity(group_id))


"""
##  REMOVIDO

notification
<class 'yowsup.layers.protocol_groups.protocolentities.notification_groups_remove.RemoveGroupsNotificationProtocolEntity'>
{'_type': 'w:gp2', 'timestamp': 1443379571, '_participant': '554896270570@s.whatsapp.net', 'participants': {'554898607439@s.whatsapp.net': None}, 'tag': 'notification', 'notify': 'Jo\xc3\xa3o Ricardo', '_from': '554896270570-1443068696@g.us', '_id': '554896270570-1443068696@g.us', 'offline': False, 'subject': 'kick admin'}

##  ADICIONADO

notification
<class 'yowsup.layers.protocol_groups.protocolentities.notification_groups_create.CreateGroupsNotificationProtocolEntity'>
{'subjectTime': 1443068696, '_type': 'w:gp2', 'createType': None, 'timestamp': 1443379650, 'creatorJid': '554896270570@s.whatsapp.net', '_participant': '554896270570@s.whatsapp.net', 'groupId': '554896270570-1443068696', 'participants': {'554896270570@s.whatsapp.net': 'admin', '554898607439@s.whatsapp.net': None}, 'tag': 'notification', 'notify': 'Jo\xc3\xa3o Ricardo', 'subjectOwnerJid': '554896270570@s.whatsapp.net', '_from': '554896270570-1443068696@g.us', '_id': '554896270570-1443068696@g.us', 'creationTimestamp': 1443068696, 'offline': False, 'subject': 'kick admin'}

##  ADICIONADO MEMBRO

notification
<class 'yowsup.layers.protocol_groups.protocolentities.notification_groups_add.AddGroupsNotificationProtocolEntity'>
{'_type': 'w:gp2', 'timestamp': 1443379735, '_participant': '554896270570@s.whatsapp.net', 'participants': ['554898050168@s.whatsapp.net'], 'tag': 'notification', 'notify': 'Jo\xc3\xa3o Ricardo', '_from': '554896270570-1443068696@g.us', '_id': '554896270570-1443068696@g.us', 'offline': False}

## REMOVIDO MEMBRO

notification
<class 'yowsup.layers.protocol_groups.protocolentities.notification_groups_remove.RemoveGroupsNotificationProtocolEntity'>
{'_type': 'w:gp2', 'timestamp': 1443380969, '_participant': '554896270570@s.whatsapp.net', 'participants': {'554899914159@s.whatsapp.net': None}, 'tag': 'notification', 'notify': 'Jo\xc3\xa3o Ricardo', '_from': '554896270570-1443068696@g.us', '_id': '554896270570-1443068696@g.us', 'offline': False, 'subject': 'kick admin'}
"""
