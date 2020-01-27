from flask import session, url_for, request
from functools import wraps

from filoLogic.SessionLogic import SessionLogic
from filoModules.Returns import Returns
from filoModules.Debug import Debug
from filoRoutes import LandingRoutes as rLanding
from filoRoutes import UserRoutes as rUser
from filoRoutes import AuthRoutes as rAuth
from filoModules.Models.Session import Session as m_Session

debug = Debug("Decorators")

def needs_to_be_guest(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        debug.print_v("on needs_to_be_guest()")
        logic_resp = SessionLogic.get()
        if not logic_resp.success:
            debug.print_e(f"needs_to_be_guest: {logic_resp.content}")
            return Returns.return_message(
                "Error connecting to the database!",
                "Please try again later!",
                5,
                rLanding.index.route_path
            )
        User_Session = logic_resp.addon_data
        User_Session: m_Session
        if User_Session.logged_in:
            debug.print_w(f"needs_to_be_guest: already registered")
            return Returns.return_message(
                "You are already registered!",
                "",
                0,
                rUser.index.route_path
            )
        return f(*args, **kwargs)
    return decorated_function
def needs_to_be_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logic_resp = SessionLogic.get()
        if not logic_resp.success:
            return Returns.return_message(
                "Error connecting to the database!",
                "Please try again later!",
                5,
                rLanding.index.route_path
            )
        
        User_Session = logic_resp.addon_data
        User_Session: m_Session
        if not User_Session.logged_in:
            login_path = rAuth.index.route_path
            if request.path != rAuth.logout.route_path:
                login_path += f"?redirectUri={request.path}"
            return Returns.return_message("You need to be logged in!","^", 2, login_path)
        if User_Session.User is None:
            return Returns.return_message("user session is corrupted!", "Please try again!", 2, rAuth.index.route_path)
        return f(*args, **kwargs)
    return decorated_function

def update_session(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        debug.print_v("on update_session")
        debug.print_v("Updating session...")
        SessionLogic.update_session_using_db()
        return f(*args, **kwargs)
    return decorated_function


def needs_to_be_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logic_resp = SessionLogic.get()
        if not logic_resp.success:
            return Returns.return_message(
                "Error connecting to the database!",
                "Try again later!",
                5,
                rLanding.index.route_path
            )
        
        _session = logic_resp.addon_data
        _session: m_Session
        if not _session.User.is_admin:
            return Returns.return_message("You are not allowed to do this!", "^", 2, rAuth.logout.route_path)
        return f(*args, **kwargs)
    return decorated_function
