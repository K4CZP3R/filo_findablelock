import bcrypt

class Encryption:
    @staticmethod
    def encrypt_password(input_str: str):
        salt = bcrypt.gensalt()
        try:
            hashed = bcrypt.hashpw(input_str.encode("ASCII"), salt)
        except TypeError:
            hashed = bcrypt.hashpw(input_str, salt)
        return hashed
    
    @staticmethod
    def verify_password(input_str:str, hashed):
        try:
            return hashed == bcrypt.hashpw(input_str.encode("ASCII"), hashed)
        except TypeError:
            return hashed == bcrypt.hashpw(input_str, hashed)