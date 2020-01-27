from flask import Blueprint, render_template, request, url_for, session


from filoLogic.AdminLogic import ViewAdminLogic, AdminLogic
from filoModules.Debug import Debug
from filoModules.Returns import Returns
from filoRoutes import AdminRoutes as r
from filoModules.Models.User import User as m_User
from filoModules.Models.User import UserEntries as m_UserEntries
from filoModules.Models.Findlock import Findlock as m_Findlock
from filoModules.Models.Findlock import FindlockEntries as m_FindlockEntries
from filoModules import Decorators

import uuid
import time

AdminView = Blueprint("AdminView", __name__)
debug = Debug("AdminView")

@AdminView.route(r.logs.route_path, methods=r.logs.http_types)
@Decorators.needs_to_be_logged_in
@Decorators.needs_to_be_admin
def logs():
    logic_resp = ViewAdminLogic.get_raw_logs()
    if not logic_resp.success:
        return render_template("admin/logs.html", logs=f"Error. {logic_resp.content}")
    return render_template("admin/logs.html", logs=logic_resp.addon_data)

@AdminView.route(r.view_logs.route_path, methods=r.view_logs.http_types)
@Decorators.needs_to_be_logged_in
@Decorators.needs_to_be_admin
def view_logs():
    return render_template("admin/view_logs.html", AdminRoutes=r)

@AdminView.route(r.wipe_col.route_path, methods=r.wipe_col.http_types)
@Decorators.needs_to_be_logged_in
@Decorators.needs_to_be_admin
def wipe_action(col):
    logic_resp = ViewAdminLogic.wipe_collection(col)
    if not logic_resp.success:
        return Returns.return_message("Something went wrong!", logic_resp.content, 2, r.index.route_path)
    return Returns.return_message("Executed.", logic_resp.content, 2, r.index.route_path)

@AdminView.route(r.db_options.route_path, methods=r.db_options.http_types)
@Decorators.needs_to_be_logged_in
@Decorators.needs_to_be_admin
def db_options():
    return render_template("admin/db_options.html", AdminRoutes=r)

@AdminView.route(r.index.route_path, methods=r.index.http_types)
@Decorators.needs_to_be_logged_in
@Decorators.needs_to_be_admin
def index():
    return render_template('admin/index.html', AdminRoutes=r)

@AdminView.route(r.findlocks.route_path, methods=r.findlocks.http_types)
@Decorators.needs_to_be_logged_in
@Decorators.needs_to_be_admin
def findlocks():
    debug.print_v("On findlocks()")
    return render_template('admin/findlocks.html',
                           Findlocks=AdminLogic.get_list_of_findlocks().addon_data,
                           FindlocksEntires=AdminLogic.get_list_of_findlock_entries())


@AdminView.route(r.findlock.route_path, methods=r.findlock.http_types)
@Decorators.needs_to_be_logged_in
@Decorators.needs_to_be_admin
def findlock(fl_uuid):
    debug.print_v(f"on findlock with fl_uuid:{fl_uuid}")
    logic_resp = ViewAdminLogic.get_findlock_info(fl_uuid)
    if not logic_resp.success:
        return Returns.return_message("Something went wrong!", logic_resp.content, 2, r.findlocks.route_path)
    _findlock = logic_resp.addon_data
    _findlock: m_Findlock

    logic_resp = ViewAdminLogic.get_findlock_entries()
    if not logic_resp.success:
        return Returns.return_message("Something went wrong!", logic_resp.content, 2, r.findlocks.route_path)
    _findlock_entries = logic_resp.addon_data
    
    
    return render_template('admin/findlock.html', findlock=_findlock, findlock_dict=_findlock.toDict(),findlock_entries=_findlock_entries)

@AdminView.route(r.findlock_update.route_path, methods=r.findlock_update.http_types)
@Decorators.needs_to_be_logged_in
@Decorators.needs_to_be_admin
def findlock_update(fl_uuid):
    logic_resp = ViewAdminLogic.findlock_update(fl_uuid, request.form)
    if not logic_resp.success:
        return Returns.return_message("Something went wrong!", logic_resp.content, 2, r.custom_findlock(fl_uuid))
    return Returns.return_message("Updated!", "Findlock data has been updated!", 2, r.custom_findlock(fl_uuid))



@AdminView.route(r.findlock_delete.route_path, methods=r.findlock_delete.http_types)
@Decorators.needs_to_be_logged_in
@Decorators.needs_to_be_admin
def findlock_delete(fl_uuid):
    debug.print_v(f"on findlock_delete with fl_uuid:{fl_uuid}")
    logic_resp = ViewAdminLogic.findlock_delete(fl_uuid)
    if not logic_resp.success:
        debug.print_e(logic_resp.content)
        return Returns.return_message("Something went wrong!", logic_resp.content, 2,r.custom_findlock(fl_uuid))
    return Returns.return_message("Deleted!", "", 1, r.findlocks.route_path)

@AdminView.route(r.findlock_add_gps.route_path, methods=r.findlock_add_gps.http_types)
@Decorators.needs_to_be_logged_in
@Decorators.needs_to_be_admin
def findlock_add_gps(fl_uuid):
    if request.method == 'GET':
        return render_template('admin/findlock_add_gps.html')
    debug.print_v(f"on findlock_add_gps with fl_uuid:{fl_uuid} | form_data: {request.form}" )

    logic_resp = ViewAdminLogic.add_gps_loc_to_findlock(fl_uuid, request.form)
    if not logic_resp.success:
        return Returns.return_message("Something went wrong!", logic_resp.content, 2,r.custom_findlock(fl_uuid))
    return Returns.return_message("Added!", "ok!",2, r.custom_findlock(fl_uuid))


@AdminView.route(r.users.route_path, methods=r.users.http_types)
@Decorators.needs_to_be_logged_in
@Decorators.needs_to_be_admin
def users():
    debug.print_v("on users")
    logic_resp_users = ViewAdminLogic.get_list_of_users()
    logic_resp_entries = ViewAdminLogic.get_list_of_user_entries()
    if not logic_resp_users.success:
        return Returns.return_message(
            "Something went wrong!",
            logic_resp_users.content,
            2, r.index.route_path
        )
    
    return render_template('admin/users.html',
                           Users=logic_resp_users.addon_data,
                           UsersEntries=logic_resp_entries
                           )


@AdminView.route(r.user.route_path, methods=r.user.http_types)
@Decorators.needs_to_be_logged_in
@Decorators.needs_to_be_admin
def user(u_uuid):
    debug.print_v(f"on user with u_uuid:{u_uuid}")
    logic_resp = ViewAdminLogic.get_user_info(u_uuid)
    if not logic_resp.success:
        return Returns.return_message("Something went wrong!", logic_resp.content, 2, r.custom_user(u_uuid))
    _user = logic_resp.addon_data
    _user: m_User

    logic_resp = ViewAdminLogic.get_user_entries()
    if not logic_resp.success:
        return Returns.return_message("Something went wrong!", logic_resp.content, 2, r.custom_user(u_uuid))
    _user_entries = logic_resp.addon_data
    
    return render_template('admin/user.html', user=_user, user_dict=_user.toDict(),user_entries=_user_entries)

@AdminView.route(r.user_update.route_path, methods=r.user_update.http_types)
@Decorators.needs_to_be_logged_in
@Decorators.needs_to_be_admin
def user_update(u_uuid):
    logic_resp = ViewAdminLogic.user_update(u_uuid, request.form)
    if not logic_resp.success:
        return Returns.return_message("Something went wrong!", logic_resp.content, 2, r.users.route_path)
    return Returns.return_message("Updated!", "User data has been updated!", 2, r.custom_user(u_uuid))

@AdminView.route(r.user_delete.route_path, methods=r.user_delete.http_types)
@Decorators.needs_to_be_logged_in
@Decorators.needs_to_be_admin
def user_delete(u_uuid):
    debug.print_v(f"user_delete on u_uuid:{u_uuid}")
    logic_resp = ViewAdminLogic.user_delete(u_uuid)
    if not logic_resp.success:
        debug.print_e(logic_resp.content)
        return Returns.return_message("Something went wrong!", logic_resp.content, 2, r.custom_user(u_uuid)) #fix me in de toekomst
    return Returns.return_message("Deleted!", "User has been deleted!", 0, r.users.route_path)

@AdminView.route(r.user_send_mail.route_path, methods=r.user_send_mail.http_types)
@Decorators.needs_to_be_logged_in
@Decorators.needs_to_be_admin
def user_send_mail(u_uuid):
    logic_resp = ViewAdminLogic.user_send_mail(u_uuid, request.form)
    if not logic_resp.success:
        return Returns.return_message("Something went wrong!", logic_resp.content, 2, r.custom_user(u_uuid))
    return Returns.return_message("Email sent!", "", 2, r.custom_user(u_uuid))