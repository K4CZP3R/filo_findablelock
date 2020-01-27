from flask import Flask, redirect, url_for, session, render_template, abort
from flask_session import Session

import config
import debug_data
import sys

from filoViews.RestView import RestView
from filoViews.LandingView import LandingView
from filoViews.AuthView import AuthView
from filoViews.UserView import UserView
from filoViews.AdminView import AdminView

from filoLogic.UserLogic import UserLogic
from filoLogic.RestLogic import RestLogic

from filoModules.Database.Handler import Handler
from filoModules.Database.User import User as db_User
from filoModules.Database.Findlock import Findlock as db_Findlock
from filoModules.Models.GpsLocation import GpsLocation as m_GpsLocation
from filoModules.Models.Findlock import Findlock as m_Findlock
from filoModules.Models.Findlock import FindlockUpdateTypes as m_FindlockUpdateTypes
from filoModules.Debug import Debug
from werkzeug.exceptions import HTTPException

debug = Debug("app.py")
debug.print_v("="*16)
debug.print_v("= Filo Server")
debug.print_v("="*16)

app = Flask(__name__)
app_blueprints = [RestView, LandingView, AuthView, UserView, AdminView]
for b in app_blueprints:
    app.register_blueprint(b)


app.config.from_object(config.get_flask_conf_obj())
Session(app)

debug.reset_log()
@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    e: Exception
    debug.print_e("="*32)
    debug.print_e("WE HAVE CRASHED")
    debug.print_e(f"{e}")
    debug.print_e("="*32)

    return internal_server_error(e)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('default/error.html', code=404, message="Endpoint bestaat niet", e=e)


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('default/error.html', code=500, message="Server side is kapot", e=e)


@app.route('/tos')
def tos():
    return render_template('landing/tos.html')


@app.route('/pp')
def pp():
    return render_template('landing/tos.html')


def recreate_debug_environment():
    debug.print_w("Dropping all")
    debug.print_i(db_Findlock().drop_all())

    debug.print_i("Creating dummmy user!")
    debug.print_i(db_User().create_user(
        debug_data.get_dummy_user()
    ))
    debug.print_i("Creating dummy user with permissions")
    debug.print_i(db_User().create_user(
        debug_data.get_dummy_user_with_permissions()
    ))

    debug.print_i("Adding dummy user w/ permissions to dummy findlock")

    dummy_findlock = debug_data.get_dummy_findlock()
    debug.print_i(dummy_findlock.FindlockPermission.addAllowedUuid(
        debug_data.get_dummy_user_with_permissions().user_uuid
    ))

    debug.print_i("Creating dummmy findlock!")
    debug.print_i(db_Findlock().create_findlock(
        dummy_findlock
    ))

    debug.print_i("Pairing dummy findlock with dummy user!")
    debug.print_i(UserLogic.pair_with_findlock(
        dummy_findlock.device_uuid,
        dummy_findlock.master_pincode,
        debug_data.get_dummy_user().user_uuid
    ))

    debug.print_i("Sending dummy GPS location to dummy findlock")
    debug.print_i(RestLogic.update_findlock(
        dummy_findlock.device_uuid,
        m_FindlockUpdateTypes.gps_location,
        debug_data.get_dummy_location().__dict__
    ))


if __name__ == "__main__":
    debug.print_d(
        f"Starting server at {config.get_flask_addr().get_connected()}")
    debug.print_d(f"Production mode: {config.is_prod()}")

    #if not config.is_prod():
    #    recreate_debug_environment()
    
    app.run(
        host=config.get_flask_addr().address,
        port=config.get_flask_addr().port,
        debug=(not config.is_prod()),
        ssl_context=config.get_ssl_context()
    )
