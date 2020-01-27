from flask import session
from filoModules.Database.User import User as db_User
from filoModules.Models.LogicReturn import LogicReturn as m_LogicReturn
from filoModules.Models.User import User as m_User
from filoModules.Models.User import UserEntries as m_UserEntries
from filoModules.Models.Session import Session as m_Session


class SessionLogic:
    @staticmethod
    def get() -> m_LogicReturn:
        user_session = m_Session.fromSession(session)
        return m_LogicReturn.f_success("Got data!", user_session)

    @staticmethod
    def logout() -> m_LogicReturn:
        user_session = m_Session.fromSession(session)
        user_session.logged_in = False
        session['filo'] = user_session.toDict()
        return m_LogicReturn.f_success_msg("Session updated!")

    @staticmethod
    def login(User: m_User) -> m_LogicReturn:
        user_session = m_Session.fromSession(session)
        user_session.logged_in = True
        user_session.User = User
        session['filo'] = user_session.toDict()
        return m_LogicReturn.f_success_msg("Session updated!")

    @staticmethod
    def update_session_using_db() -> m_LogicReturn:
        user_session = m_Session.fromSession(session)
        db_resp = db_User().get_user(
            m_UserEntries.user_uuid,
            user_session.User.user_uuid
        )

        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)

        User = db_resp.addon_data
        User: m_User

        user_session.User = User
        session['filo'] = user_session.toDict()
        return m_LogicReturn.f_success_msg("Session updated!")
