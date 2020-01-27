class EventEntries:
    _type = 'type'
    created_at = 'created_at'
    executed = 'executed'

class EventTypes:
    unlock = "unlock"
    lock = "lock"
    light = "light"
    
class Event(object):
    def __init__(self, _type, _created_at, _executed=False):
        self.type = _type
        self.created_at = _created_at
        self.executed = _executed
    @classmethod
    def empty(cls):
        return cls(None, None)

    def change_execution(self, new_value: bool):
        self.executed = new_value

    @classmethod
    def fromDict(cls, input_dict: dict):
        return cls(
            input_dict[EventEntries._type],
            input_dict[EventEntries.created_at],
            input_dict[EventEntries.executed]
        )

    def toDict(self):
        return {
            EventEntries._type: self.type,
            EventEntries.created_at: self.created_at,
            EventEntries.executed: self.executed
        }
