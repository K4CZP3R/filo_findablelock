import json


class LogicReturnEntries:
    success = "success"
    content = "content"
    addon_data = "addon_data"

class LogicReturn(object):
    def __init__(self, success, content, addon_data):
        self.success = success
        self.content = content
        self.addon_data = addon_data
    
    @classmethod
    def f_error_msg(cls, msg):
        return cls(False, msg, None)
    
    @classmethod
    def f_error(cls, msg, data):
        return cls(False, msg, data)
    
    @classmethod
    def f_success_msg(cls, msg):
        return cls(True, msg, None)
    
    @classmethod
    def f_success(cls, msg, data):
        return cls(True, msg, data)
    
    def __toDict(self) -> dict:
        return {
            LogicReturnEntries.success: self.success,
            LogicReturnEntries.content: self.content,
            LogicReturnEntries.addon_data: self.addon_data
        }

    def toJStr(self) -> str:
        return json.dumps(self.__toDict())
