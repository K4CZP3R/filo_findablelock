from flask import Blueprint, render_template, session, redirect, render_template, url_for, request
from filoLogic.UserLogic import ViewUserLogic
from filoModules.Debug import Debug
from filoModules.Returns import Returns
from filoModules import Decorators
from filoRoutes import UserRoutes as r
from filoRoutes import AuthRoutes as rAuth
from filoLogic.SessionLogic import SessionLogic
from filoModules.Models.Session import Session as m_Session
from filoModules.Models.Findlock import Findlock as m_Findlock
UserView = Blueprint("UserView", __name__)

debug = Debug("UserView")



@UserView.route(r.add_friend.route_path, methods=r.add_friend.http_types)
@Decorators.needs_to_be_logged_in
@Decorators.update_session
def add_friend():
    if request.method == 'GET':
        return render_template("webapp/user/confirm.html")

    logic_resp = SessionLogic.get()
    if not logic_resp.success:
        return Returns.return_message("Something went wrong!", logic_resp.content, 2, r.index.route_path)
    _session = logic_resp.addon_data
    _session: m_Session
    print(request.form)
    logic_resp = ViewUserLogic.add_friend(_session, request.form)
    if not logic_resp.success:
        return Returns.return_message("Failed to add a friend!", logic_resp.content, 2, r.index.route_path)
    return Returns.return_message("Friend added!", logic_resp.content, 2, r.index.route_path)
    

@UserView.route(r.index.route_path, methods=r.index.http_types)
@Decorators.needs_to_be_logged_in
@Decorators.update_session
def index():
    logic_resp = SessionLogic.get()
    if not logic_resp.success:
        return Returns.return_message("Something went wrong!", logic_resp.content, 2, r.index.route_path)

    _session = logic_resp.addon_data
    _session: m_Session

    logic_resp = ViewUserLogic.user_data_is_missing(_session)
    if logic_resp.success:  # account misses some data
        return redirect(r.update.route_path)

    logic_resp = ViewUserLogic.get_user_findlocks(_session)
    if not logic_resp.success:
        return Returns.return_message("Failed!", logic_resp.content, 2, rAuth.logout.route_path)
    print(logic_resp.addon_data)
    return render_template("webapp/user/profile.html", Session=_session, findlocks=logic_resp.addon_data, findlocks_n=len(logic_resp.addon_data))
    #return render_template("user/index.html", Session=_session, findlocks=logic_resp.addon_data, AuthRoutes=rAuth)


@UserView.route(r.update.route_path, methods=r.update.http_types)
@Decorators.needs_to_be_logged_in
@Decorators.update_session
def update():
    logic_resp = SessionLogic.get()
    if not logic_resp.success:
        return Returns.return_message("Something went wrong!", logic_resp.content, 2, r.index.route_path)
    _session = logic_resp.addon_data
    _session: m_Session

    if request.method == 'POST':
        logic_resp = ViewUserLogic.update_user_data(_session, request.form)
        if not logic_resp.success:
            return Returns.return_message("Something went wrong!", logic_resp.content, 2, r.index.route_path)
        return redirect(r.index.route_path)

    logic_resp = ViewUserLogic.user_data_is_missing(_session)
    if not logic_resp.success:
        return Returns.return_message("Something went wrong", logic_resp.content, 2, r.index.route_path)
    return render_template('user/fill_in_data.html', missing_data=logic_resp.addon_data)


@UserView.route(r.new_device.route_path, methods=r.new_device.http_types)
@Decorators.needs_to_be_logged_in
@Decorators.update_session
def new_device():
    logic_resp = SessionLogic.get()
    if not logic_resp.success:
        return Returns.return_message("Something went wrong!", logic_resp.content, 2, r.index.route_path)
    _session = logic_resp.addon_data
    _session: m_Session

    if request.method == 'GET':
        return render_template('user/new_device.html')

    logic_resp = ViewUserLogic.pair_with_findlock(
        _session, request.form
    )
    if not logic_resp.success:
        return Returns.return_message("Something went wrong!", logic_resp.content, 2, r.index.route_path)
    return Returns.return_message("Paired!", "Nice!", 2, r.index.route_path)


@UserView.route(r.device.route_path, methods=r.device.http_types)
@Decorators.needs_to_be_logged_in
@Decorators.update_session
def device(d_uuid):
    logic_resp = SessionLogic.get()
    if not logic_resp.success:
        return Returns.return_message("Something went wrong!", logic_resp.content, 2, r.index.route_path)
    _session = logic_resp.addon_data
    _session: m_Session

    logic_resp = ViewUserLogic.user_allowed_to_use_findlock(_session, d_uuid)
    if not logic_resp.success:
        return Returns.return_message("Something went wrong!", logic_resp.content, 2,r.index.route_path)

    logic_resp  = ViewUserLogic.get_findlock_info(d_uuid)
    if not logic_resp.success:
        return Returns.return_message("Something went wrong!", logic_resp.content, 2, r.index.route_path)
    _findlock = logic_resp.addon_data
    _findlock: m_Findlock
    #return render_template("user/device.html", findlock=_findlock, session=_session)
    return render_template("webapp/user/home.html", findlock=_findlock, session=_session)

@UserView.route(r.lock_unlock_screen.route_path, methods=r.lock_unlock_screen.http_types)
@Decorators.needs_to_be_logged_in
@Decorators.update_session
def lock_unlock_screen(d_uuid):
    return render_template("webapp/user/lock-unlock.html", device_uuid=d_uuid)

@UserView.route(r.light_screen.route_path, methods=r.light_screen.http_types)
@Decorators.needs_to_be_logged_in
@Decorators.update_session
def light_screen(d_uuid):
    return render_template("webapp/user/light.html", device_uuid=d_uuid)

@UserView.route(r.settings_screen.route_path, methods=r.settings_screen.http_types)
@Decorators.needs_to_be_logged_in
@Decorators.update_session
def settings_screen():
    logic_resp = SessionLogic.get()
    if not logic_resp.success:
        return Returns.return_message("Something went wrong!", logic_resp.content, 2, r.index.route_path)
    _session = logic_resp.addon_data
    _session: m_Session
    return render_template("webapp/user/settings.html", session=_session)


@UserView.route(r.fingerprints_screen.route_path, methods=r.fingerprints_screen.http_types)
@Decorators.needs_to_be_logged_in
@Decorators.update_session
def fingerprints_screen(d_uuid):
    logic_resp = SessionLogic.get()
    if not logic_resp.success:
        return Returns.return_message("Something went wrong!", logic_resp.content, 2, r.index.route_path)
    _session = logic_resp.addon_data
    _session: m_Session

    logic_resp = ViewUserLogic.get_allowed_users_for_findlock(d_uuid)
    if not logic_resp.success:
        return Returns.return_message("Something went wrong!", logic_resp.content, 2, r.index.route_path)
    
    list_of_names = logic_resp.addon_data


    return render_template("webapp/user/fingerprint.html", list_of_names=list_of_names)