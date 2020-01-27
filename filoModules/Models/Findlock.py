import uuid
from filoModules.Models.GpsLocation import GpsLocation
from filoModules.Models.Event import Event
from filoModules.Models.FindlockPermission import FindlockPermission
from filoModules.Models.GpsLocationHistory import GpsLocationHistory
    

class FindlockUpdateTypes:
    gps_location = "gps_location"

class FindlockEntries:
    friendly_name = "friendly_name"
    GpsLocationHistory = "GpsLocationHistory"
    master_pincode = 'master_pincode'
    Event = 'Event'
    device_uuid = "device_uuid"
    FindlockPermission = 'FindlockPermission'


class Findlock(object):
    def __init__(self, friendly_name, GpsLocationHistory: GpsLocationHistory, master_pincode, Event: Event, FindlockPermission: FindlockPermission, device_uuid=str(uuid.uuid4())):
        self.friendly_name = friendly_name
        self.GpsLocationHistory = GpsLocationHistory
        self.master_pincode = master_pincode
        self.Event = Event
        self.FindlockPermission = FindlockPermission
        self.device_uuid = device_uuid

    @classmethod
    def fromDict(cls, input_dict: dict):
        return cls(
            input_dict[FindlockEntries.friendly_name],
            GpsLocationHistory.fromDict(
                input_dict[FindlockEntries.GpsLocationHistory]),
            input_dict[FindlockEntries.master_pincode],
            Event.fromDict(input_dict[FindlockEntries.Event]),
            FindlockPermission.fromDict(
                input_dict[FindlockEntries.FindlockPermission]),
            device_uuid=input_dict[FindlockEntries.device_uuid]
        )

    def toDict(self):
        return {
            FindlockEntries.friendly_name: self.friendly_name,
            FindlockEntries.GpsLocationHistory: self.GpsLocationHistory.toDict(),
            FindlockEntries.master_pincode: self.master_pincode,
            FindlockEntries.Event: self.Event.toDict(),
            FindlockEntries.FindlockPermission: self.FindlockPermission.toDict(),
            FindlockEntries.device_uuid: self.device_uuid
        }
