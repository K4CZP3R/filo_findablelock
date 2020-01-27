import re, uuid
from filoModules.Models.LogicReturn import LogicReturn as m_LogicReturn


class Verifier:
    @staticmethod
    def verify_email(email_input) -> bool:
        regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,8})+$'
        if(re.search(regex, email_input)):
            return True
        return False
    @staticmethod
    def verify_friendcode(friend_code_input) -> m_LogicReturn:
        allowed_code_chars = "0123456789"
        allowed_splitter_char = "#"
        allowed_code_len = 4

    
        friend_code_input = str(friend_code_input)
        if not allowed_splitter_char in friend_code_input:
            return m_LogicReturn.f_error_msg(f"Invalid friendcode (missing '{allowed_splitter_char}')")
        
        friend_code_splitted = friend_code_input.split(allowed_splitter_char)
        if len(friend_code_splitted) != 2:
            return m_LogicReturn.f_error_msg("Invalid friendcode (splitted != 2)")
        
        code = friend_code_splitted[1]

        if len(code) != allowed_code_len:
            return m_LogicReturn.f_error_msg(f"Invalid friendcode (code len != {allowed_code_len})")
        
        for c in code:
            if c not in allowed_code_chars:
                return m_LogicReturn.f_error_msg(f"Invalid friendcode (code contains illegal char: '{c}')")
            
        return m_LogicReturn.f_success_msg("Valid friendcode!")

    @staticmethod
    def verify_password(password_input) -> m_LogicReturn:
        password_input = str(password_input)
        if len(password_input) < 8 or len(password_input) > 16:
            return m_LogicReturn.f_error_msg("Password is too long or too short (min: 8, max: 16)")
        if not any(char.isdigit() for char in password_input):
            return m_LogicReturn.f_error_msg("Password should contain atleast one digit")
        return m_LogicReturn.f_success_msg("Password is valid!")
    @staticmethod
    def verify_uuid(uuid_input) -> m_LogicReturn:
        try:
            uuid.UUID(f"{uuid_input}")
            return m_LogicReturn.f_success_msg("Valid uuid!")
        except ValueError:
            return m_LogicReturn.f_error_msg("Invalid uuid!")
    @staticmethod
    def value_empty(i) -> bool:
        if i == None:
            return True
        if f"{i}" == "":
            return True
        if len(f"{i}") <= 0:
            return True
        return False
