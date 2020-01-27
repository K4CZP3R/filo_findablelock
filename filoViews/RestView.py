from flask import Blueprint, render_template, session, redirect, request, jsonify

from filoLogic.RestLogic import ViewRestLogic
from filoModules.Models.ApiReturn import ApiReturn
from filoModules.Debug import Debug
from filoRoutes import RestRoutes as r
from filoModules import Decorators
import json

from filoRoutes import AdminRoutes, AuthRoutes, LandingRoutes, RestRoutes, UserRoutes

RestView = Blueprint("RestView", __name__)
debug = Debug("RestView")

@RestView.route(r.get_last_location.route_path, methods=r.get_last_location.http_types)
def get_last_location(device_uuid):
    logic_resp = ViewRestLogic.get_findlock_location(device_uuid)
    if not logic_resp.success:
        return ApiReturn.f_error(logic_resp.content).toFlask()
    return jsonify(logic_resp.addon_data)
    
@RestView.route(r.get_name_by_uuid.route_path, methods=r.get_name_by_uuid.http_types)
def get_name_by_uuid(i_uuid):
    logic_resp = ViewRestLogic.get_name_by_uuid(i_uuid)
    if not logic_resp.success:
        return ApiReturn.f_error(logic_resp.content).toFlask()
    return ApiReturn.f_success(logic_resp.content).toFlask()


@RestView.route(r.light_front.route_path, methods=r.light_front.http_types)
@Decorators.needs_to_be_logged_in
def light_front(device_uuid):
    logic_resp = ViewRestLogic.light_findlock_frontend(device_uuid)
    if not logic_resp.success:
        return ApiReturn.f_error(logic_resp.content).toFlask()
    return ApiReturn.f_success(logic_resp.content).toFlask()


@RestView.route(r.light.route_path, methods=r.light.http_types)
def light():
    debug.print_v(f"on light()")
    logic_resp = ViewRestLogic.light_findlock(request.form)
    if logic_resp.success:
        return ApiReturn.f_error(logic_resp.content).toFlask()
    return ApiReturn.f_success(logic_resp.content).toFlask()


@RestView.route(r.change_state_front.route_path, methods=r.change_state_front.http_types)
def change_state_front(device_uuid, state):
    #state: lock or unlock
    logic_resp = ViewRestLogic.change_findlock_state_frontend(
        device_uuid,
        state
    )
    if not logic_resp.success:
        return ApiReturn.f_error(logic_resp.content).toFlask()
    return ApiReturn.f_success(logic_resp.success).toFlask()


@RestView.route(r.get_state_front.route_path, methods=r.get_state_front.http_types)
def get_state_front(device_uuid):
    logic_resp = ViewRestLogic.get_findlock_state_frontend(device_uuid)
    if not logic_resp.success:
        return ApiReturn.f_error(logic_resp.content).toFlask()
    return ApiReturn.f_success(logic_resp.addon_data).toFlask()


@RestView.route(r.unlock.route_path, methods=r.unlock.http_types)
def unlock_nfc():
    # unlock using nfc id
    logic_resp = ViewRestLogic.unlock_findlock_nfc(
        request.form
    )

    if not logic_resp.success:
        return ApiReturn.f_error(logic_resp.content).toFlask()
    return ApiReturn.f_success(logic_resp.content).toFlask()


@RestView.route(r.lock.route_path, methods=r.lock.http_types)
def lock_nfc():
    # lock using nfc id
    logic_resp = ViewRestLogic.lock_findlock_nfc(
        request.form
    )

    if not logic_resp.success:
        return ApiReturn.f_error(logic_resp.content).toFlask()
    return ApiReturn.f_success(logic_resp.content).toFlask()


@RestView.route(r.unlock_fp.route_path, methods=r.unlock_fp.http_types)
def unlock_fingerprint():
    # lock using nfc id
    logic_resp = ViewRestLogic.unlock_findlock_fingerprint(
        request.form
    )

    if not logic_resp.success:
        return ApiReturn.f_error(logic_resp.content).toFlask()
    return ApiReturn.f_success(logic_resp.content).toFlask()


@RestView.route(r.lock_fp.route_path, methods=r.lock_fp.http_types)
def lock_fingerprint():
    # lock using nfc id
    logic_resp = ViewRestLogic.lock_findlock_fingerprint(
        request.form
    )

    if not logic_resp.success:
        return ApiReturn.f_error(logic_resp.content).toFlask()
    return ApiReturn.f_success(logic_resp.content).toFlask()


@RestView.route(r.events_update.route_path, methods=r.events_update.http_types)
def events_update():
    logic_resp = ViewRestLogic.update_findlock_event(request.form)
    if not logic_resp.success:
        return ApiReturn.f_error(logic_resp.content).toFlask()
    return ApiReturn.f_success(logic_resp.content).toFlask()


@RestView.route(r.events_get.route_path, methods=r.events_get.http_types)
def events_get():
    logic_resp = ViewRestLogic.get_findlock_event(request.form)
    if not logic_resp.success:
        return ApiReturn.f_error(logic_resp.content).toFlask()
    return ApiReturn.f_success(logic_resp.addon_data).toFlask()


@RestView.route(r.index.route_path, methods=r.index.http_types)
def index():
    return ApiReturn.f_success("Hello, World!").toFlask()


@RestView.route(r.findlock_get.route_path, methods=r.findlock_get.http_types)
def get_findlock():
    logic_resp = ViewRestLogic.get_findlock(
        request.form
    )
    if not logic_resp.success:
        return ApiReturn.f_error(logic_resp.content).toFlask()
    return ApiReturn.f_success(logic_resp.addon_data).toFlask()


@RestView.route(r.findlock_update.route_path, methods=r.findlock_update.http_types)
def update_findlock():
    logic_resp = ViewRestLogic.update_findlock(
        request.form
    )
    if not logic_resp.success:
        return ApiReturn.f_error(logic_resp.content).toFlask()
    return ApiReturn.f_success(logic_resp.success).toFlask()


@RestView.route(r.routing_js.route_path, methods=r.routing_js.http_types)
def routing_js():

    default_device_uuid = "00000000-0000-0000-0000-000000000001"
    js_func = """\
    function change_frontend(class_name, route)
    {
        var elements = document.getElementsByClassName(class_name);
        var elementsArray = Array.prototype.slice.call(elements)

        elementsArray.forEach(function(value, index, ar){
            console.log("Replaced "+class_name+" to '"+route+"'")
            elements[index].onclick = function(){location.href = route}
        })
    }"""

    js_cmds = f"""\
    change_frontend("onclick_auth_register", "{AuthRoutes.register.route_path}")
    change_frontend("onclick_auth", "{AuthRoutes.index.route_path}")

    change_frontend("onclick_home", "{UserRoutes.custom_device(default_device_uuid)}")
    change_frontend("onclick_fingerprint", "{UserRoutes.custom_fingerprints_screen(default_device_uuid)}")
    change_frontend("onclick_profile", "{UserRoutes.index.route_path}")
    change_frontend("onclick_lock", "{UserRoutes.custom_lock_unlock_screen(default_device_uuid)}")
    change_frontend("onclick_light", "{UserRoutes.custom_light_screen(default_device_uuid)}")
    change_frontend("onclick_settings", "{UserRoutes.settings_screen.route_path}")
    change_frontend("onclick_logout", "{AuthRoutes.logout.route_path}")
    change_frontend("onclick_admin_menu", "{AdminRoutes.index.route_path}")

    """
    return js_func + js_cmds
