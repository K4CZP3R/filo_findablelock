from itsdangerous import URLSafeTimedSerializer
import config

class Token:
    @staticmethod
    def generate_confirm_token(email):
        serializer = URLSafeTimedSerializer(config.get_app_secret())
        return serializer.dumps(email, salt=config.get_security_password_salt())
    
    @staticmethod
    def confirm_token(token, expiration=3600):
        serializer = URLSafeTimedSerializer(config.get_app_secret())
        try:
            email = serializer.loads(
                token,
                salt=config.get_security_password_salt(),
                max_age=expiration
            )
        except:
            return False
        return email