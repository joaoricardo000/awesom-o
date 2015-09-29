class Group():
    def __init__(self):
        self.id = None
        self.users = []
        self.subject = None
        self.creator = None
        self.creation = None
        self.admins = []


class User():
    def __init__(self, jid=None, name=None):
        self.jid = jid
        self.name = name

    def __str__(self):
        return self.__dict__.__str__()


def parseGroupListMessage(listGroupsResultIqProtocolEntity):
    groups = []
    group_list = listGroupsResultIqProtocolEntity.getGroups()
    for g in group_list:
        group = Group()
        group.id = g.getId()
        group.subject = g.getSubject()
        group.creator = g.getCreator()
        group.creation = g.getCreationTime()
        for jid, isAdmin in g.getParticipants().iteritems():
            group.users.append(jid)
            if isAdmin:
                group.admins.append(jid)
        groups.append(group)
    return groups
