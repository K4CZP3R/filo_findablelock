import json
from flask import jsonify

class ApiReturn(object):
    def __init__(self, success, data, error):
        self.success = success
        self.data = data
        self.error = error
    
    @classmethod
    def f_success(cls, data):
        return cls(True, data, None)
    
    @classmethod
    def f_error(cls, error):
        return cls(False, None, error)
    
    def toFlask(self):
        return jsonify(self.__dict__)
    
