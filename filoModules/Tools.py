import os
import datetime
import uuid
import platform
import random
import time




class Tools:
    @staticmethod
    def find_between_r( s, first, last ):
        try:
            start = s.rindex( first ) + len( first )
            end = s.rindex( last, start )
            return s[start:end]
        except ValueError:
            return ""
    @staticmethod
    def generate_friend_code():
        return Tools.generate_random_code("0123456789", 4)
    @staticmethod
    def generate_random_code(allowed_chars, length):
        code = ""
        for i in range(0, length):
            code += allowed_chars[random.randint(0, len(allowed_chars)-1)]
        return code

    @staticmethod
    def get_unix_time():
        return int(time.time())

    @staticmethod
    def get_date_time_str():
        right_now = datetime.datetime.now()
        return f"{right_now.day}-{right_now.month}-{right_now.day}@{right_now.hour}:{str(right_now.minute).zfill(2)}:{right_now.second}.{right_now.microsecond}"

    @staticmethod
    def get_uuid():
        return str(uuid.uuid4())
    
    @staticmethod
    def get_types(obj: object) -> list:
        IGNORE_VALUES_BEGINNING = "__"
        valid_vals = list()
        for val in [v for v in dir(obj) if not callable(getattr(obj,v))]:
            if val.startswith(IGNORE_VALUES_BEGINNING):
                continue
            valid_vals.append(val)
        return valid_vals
    
    @staticmethod
    def read_txt_to_str(file_loc) -> str:
        f = open(file_loc, "r")
        lines = f.readlines()
        out = ""
        
        for line in lines:
            out+=line
        return out