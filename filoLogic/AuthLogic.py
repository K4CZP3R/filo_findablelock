

from filoLogic.SessionLogic import SessionLogic
from filoModules.Database.User import User as db_User

from filoModules.Encryption import Encryption
from filoLogic.SocialsLogic import SocialsLogic
from filoModules.Models.LogicReturn import LogicReturn as m_LogicReturn
from filoModules.Models.User import UserEntries as m_UserEntries
from filoModules.Models.User import User as m_User
from filoModules.Models.Session import Session as m_Session
from filoLogic.SessionLogic import SessionLogic
from filoModules.Token import Token
from filoModules.Email import Email
from filoModules.Tools import Tools
from filoModules.Verifier import Verifier as v


class ViewAuthLogic:
    @staticmethod
    def facebook_login(form_data) -> m_LogicReturn:
        userid = form_data.get('id', None)
        name = form_data.get('name', None)
        access_token = form_data.get('access_token', None)

        if v.value_empty(userid) or \
            v.value_empty(name) or \
                v.value_empty(access_token):
            return m_LogicReturn.f_error_msg("Data is missing!")

        return AuthLogic.facebook_login(
            access_token,
            name,
            userid
        )

    @staticmethod
    def google_login(form_data) -> m_LogicReturn:
        idtoken = form_data.get('idtoken', None)
        email = form_data.get('email', None)
        client_id = form_data.get('client_id', None)
        avatar_link = form_data.get('avatar_link', None)

        if v.value_empty(idtoken) \
                or v.value_empty(email) \
        or v.value_empty(client_id) \
        or v.value_empty(avatar_link):
            return m_LogicReturn.f_error_msg("Data is missing!")

        return AuthLogic.google_login(
            idtoken,
            email,
            client_id,
            avatar_link
        )

    @staticmethod
    def login(form_data) -> m_LogicReturn:
        email = form_data.get("emailInput", None)
        password = form_data.get("passwordInput", None)

        if v.value_empty(email) \
                or v.value_empty(password):
            return m_LogicReturn.f_error_msg("Data is missing!")
        return AuthLogic.login(
            email,
            password
        )
    
    @staticmethod
    def logout() -> m_LogicReturn:
        return SessionLogic.logout()
    
    @staticmethod
    def verify_confirm_code(confirm_token) -> m_LogicReturn:
        if v.value_empty(confirm_token):
            return m_LogicReturn.f_error_msg("Data is missing!")
        
        return AuthLogic.process_confirmation_code(confirm_token)
    
    @staticmethod
    def register(form_data) -> m_LogicReturn:
        user_email = form_data.get("emailInput", None)
        user_password = form_data.get("passwordInput", None)
        user_password_2 = form_data.get("passwordInput2", None)

        if v.value_empty(user_email) \
            or v.value_empty(user_password) \
                or v.value_empty(user_password_2):
                return m_LogicReturn.f_error_msg("Data is missing!")
        
        return AuthLogic.register(
            user_email,
            user_password,
            user_password_2
        )



class AuthLogic:

    @staticmethod
    def facebook_login(access_token, name, userid) -> m_LogicReturn:
        if v.value_empty(access_token) \
            or v.value_empty(name) \
                or v.value_empty(userid):
            return m_LogicReturn.f_error_msg("missing data!")

        logic_resp = SocialsLogic.fb_verify_access_token(access_token)
        if not logic_resp:
            return m_LogicReturn.f_error_msg("invalid access token")

        db_resp = db_User().get_user(
            m_UserEntries.facebook_user_id,
            userid
        )
        if not db_resp.success:
            logic_resp = AuthLogic.facebook_register(name, userid)
            if not logic_resp.success:
                return m_LogicReturn.f_error_msg(logic_resp.content)
        db_resp = db_User().get_user(
            m_UserEntries.facebook_user_id,
            userid
        )
        _User = db_resp.addon_data
        _User: m_User

        logic_resp = SessionLogic.login(_User)
        if not logic_resp.success:
            return m_LogicReturn.f_error_msg(logic_resp.content)
        return m_LogicReturn.f_success_msg("Logged in!")

    @staticmethod
    def facebook_register(name, userid) -> m_LogicReturn:
        if v.value_empty(name) or v.value_empty(userid):
            return m_LogicReturn.f_error_msg("data is missing!")
        _User = m_User(
            first_name=str(name).split(" ")[0],
            surname=str(name).split(" ")[1],
            email=None,
            password_hash=None,
            phone_number=None,
            nfc_id=None,
            finger_id=None,
            friend_code=Tools.generate_friend_code(),
            facebook_user_id=userid,
            verified=True
        )
        db_resp = db_User().create_user(_User)
        if db_resp.success:
            return m_LogicReturn.f_success_msg(db_resp.content)
        return m_LogicReturn.f_error_msg(db_resp.content)

    @staticmethod
    def google_register(google_user_id, user_email, avatar_link) -> m_LogicReturn:
        if v.value_empty(google_user_id) \
                or v.value_empty(user_email):
            return m_LogicReturn.f_error_msg("post data is missing!")

        if not v.verify_email(user_email):
            return m_LogicReturn.f_error_msg("E-mail is not valid!")

        _User = m_User(
            first_name=None,
            surname=None,
            email=user_email,
            password_hash=None,
            phone_number=None,
            nfc_id=None,
            finger_id=None,
            friend_code=Tools.generate_friend_code(),
            google_user_id=google_user_id,
            avatar_link=avatar_link,
            verified=True
        )

        db_resp = db_User().create_user(_User)
        if db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)
        return m_LogicReturn.f_success_msg(db_resp.content)

    @staticmethod
    def google_login(google_token_id, user_email, client_id, avatar_link) -> m_LogicReturn:
        if v.value_empty(google_token_id) \
            or v.value_empty(user_email) \
                or v.value_empty(client_id) \
                or v.value_empty(avatar_link):
            return m_LogicReturn.f_error_msg("Data is missing!")

        if not v.verify_email(user_email):
            return m_LogicReturn.f_error_msg("E-mail is invalid!")

        logic_resp = SocialsLogic.verify_token_id(google_token_id, client_id)
        if not logic_resp.success:
            return m_LogicReturn.f_error_msg("invalid id token")

        google_user_id = logic_resp.addon_data

        db_resp = db_User().get_user(
            m_UserEntries.google_user_id,
            google_user_id
        )
        if not db_resp.success:
            logic_resp = AuthLogic.google_register(
                google_user_id, user_email, avatar_link)
            if not logic_resp.success:
                return m_LogicReturn.f_error_msg(logic_resp.content)

        db_resp = db_User().get_user(
            m_UserEntries.google_user_id,
            google_user_id
        )
        _User = db_resp.addon_data
        _User: m_User

        logic_resp = SessionLogic.login(_User)
        if not logic_resp.success:
            return m_LogicReturn.f_error_msg(logic_resp.content)
        return m_LogicReturn.f_success_msg("Logged in!")

    @staticmethod
    def login(user_email, user_password) -> m_LogicReturn:
        if v.value_empty(user_email) \
           or v.value_empty(user_password):
            return m_LogicReturn.f_error_msg("Post data is missing!")

        if not v.verify_email(user_email):
            return m_LogicReturn.f_error_msg("E-mail is invalid!")
        v_pass = v.verify_password(user_password)
        if not v_pass.success:
            return m_LogicReturn.f_error_msg(v_pass.content)

        db_resp = db_User().get_user(
            m_UserEntries.email,
            user_email
        )

        if not db_resp.success:
            return m_LogicReturn.f_error_msg("Wrong email/password combination")

        _User = db_resp.addon_data
        _User: m_User

        if not Encryption.verify_password(
                user_password, _User.password_hash):
            return m_LogicReturn.f_error_msg("Wrong email/password combination")

        if not _User.verified:
            return m_LogicReturn.f_error_msg("User did not verify via email.")

        logic_resp = SessionLogic.login(_User)
        if not logic_resp.success:
            return m_LogicReturn.f_error_msg(logic_resp.content)
        return m_LogicReturn.f_success_msg("Logged in!")

    @staticmethod
    def process_confirmation_code(confirm_token) -> m_LogicReturn:
        email = Token.confirm_token(confirm_token)
        if email is False:
            return m_LogicReturn.f_error_msg("This link is invalid or has expired.")

        User = db_User().get_user(
            m_UserEntries.email, email
        )
        if not User.success:
            return m_LogicReturn.f_error_msg("Can't find user with this email")
        User = User.addon_data
        User: m_User

        User.verified = True

        db_resp = db_User().update_user(User)
        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)
        return m_LogicReturn.f_success_msg("User is verified now!")

    @staticmethod
    def register(user_email, user_password, user_password2) -> m_LogicReturn:
        if v.value_empty(user_email) \
            or v.value_empty(user_password) \
                or v.value_empty(user_password2):
            return m_LogicReturn.f_error_msg("post data is missing")

        v_pass = v.verify_password(user_password)
        if not v_pass.success:
            return m_LogicReturn.f_error_msg(v_pass.content)

        if not v.verify_email(user_email):
            return m_LogicReturn.f_error_msg("E-mail is invalid")

        if user_password != user_password2:
            return m_LogicReturn.f_error_msg("Passwords are not the same!")

        password_hash = Encryption.encrypt_password(
            user_password)
        _User = m_User(
            first_name=None,
            surname=None,
            email=user_email,
            password_hash=password_hash,
            phone_number=None,
            nfc_id=None,
            finger_id=None,
            friend_code=Tools.generate_friend_code(),
            avatar_link="https://www.clevelanddentalhc.com/wp-content/uploads/2018/03/sample-avatar-300x300.jpg"
        )

        db_resp = db_User().create_user(_User)
        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)
        token_code = Token.generate_confirm_token(user_email)
        print(f"Token code: {token_code}")
        email_message = Email.get_register_email(user_email, token_code)
        email_resp = Email.send_email(user_email, email_message)
        if not email_resp.success:
            return m_LogicReturn.f_error_msg("Failed to send email!")

        return m_LogicReturn.f_success_msg(db_resp.content)
