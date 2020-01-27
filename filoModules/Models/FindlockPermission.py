class FindlockPermissionEntries:
    master_uuid = 'master_uuid'
    allowed_uuids = 'allowed_uuids'


class FindlockPermission(object):
    def __init__(self, master_uuid: str, allowed_uuids: [str]):
        self.master_uuid = master_uuid
        self.allowed_uuids = allowed_uuids
    @classmethod
    def empty(cls):
        return cls(None, [])
        
    def addAllowedUuid(self, uuid_to_add):
        self.allowed_uuids.append(uuid_to_add)

    def removeAllowedUuid(self, uuid_to_remove):
        for u in self.allowed_uuids:
            if u == uuid_to_remove:
                self.allowed_uuids.pop(uuid_to_remove)

    def allowed_uuids_count(self):
        return len(self.allowed_uuids)
    @classmethod
    def fromDict(cls, input_dict: dict):
        return cls(
            input_dict[FindlockPermissionEntries.master_uuid],
            input_dict[FindlockPermissionEntries.allowed_uuids]
        )

    def toDict(self):
        return {
            FindlockPermissionEntries.master_uuid: self.master_uuid,
            FindlockPermissionEntries.allowed_uuids: self.allowed_uuids
        }
