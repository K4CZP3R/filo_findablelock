from flask import Blueprint, render_template, request, url_for, session


from filoLogic.AuthLogic import ViewAuthLogic

from filoModules.Debug import Debug
from filoModules.Returns import Returns
from filoModules import Decorators
from filoRoutes import AuthRoutes as r
from filoRoutes import UserRoutes as rUser
from filoRoutes import AuthRoutes as rAuth
from filoRoutes import LandingRoutes as rLanding
from filoModules.Models.Session import Session as m_Session


AuthView = Blueprint("AuthView", __name__)

debug = Debug("AuthView")

@AuthView.route(r.google_verify.route_path, methods=r.google_verify.http_types)
@Decorators.needs_to_be_guest
def google_verify():
    return "ok?"

@AuthView.route(r.facebook_login.route_path, methods=r.facebook_login.http_types)
@Decorators.needs_to_be_guest
def facebook_login():
    logic_resp = ViewAuthLogic.facebook_login(request.form)
    if logic_resp.success:
        return "yes"
    return "no"

@AuthView.route(r.google_login.route_path, methods=r.google_login.http_types)
@Decorators.needs_to_be_guest
def google_login():
    logic_resp = ViewAuthLogic.google_login(request.form)
    if logic_resp.success:
        return "yes"
    return "no"
    
@AuthView.route(r.index.route_path, methods=r.index.http_types)
@Decorators.needs_to_be_guest
def index():
    debug.print_v("on index()")
    if request.method == 'GET':
        debug.print_v("Sending html page back (GET)")
        return render_template('webapp/auth.html', AuthRoutes=rAuth)


    logic_resp = ViewAuthLogic.login(request.form)
    if not logic_resp.success:
        debug.print_e(logic_resp.content)
        return Returns.return_message(
            "Something went wrong!", logic_resp.content, 2,r.index.route_path
        )
    print(request.args.get("redirectUri",None))

    #check if redirectUri is here
    redirect_override_url = request.args.get("redirectUri", None)
    redirect_to = redirect_override_url if redirect_override_url is not None else rUser.index.route_path
    return Returns.return_message("Message", logic_resp.content, 1, redirect_to)


@AuthView.route(r.logout.route_path, methods=r.logout.http_types)
@Decorators.needs_to_be_logged_in
def logout():
    debug.print_v("on logout()")
    logic_resp =  ViewAuthLogic.logout()
    if not logic_resp.success:
        return Returns.return_message(
            "Something went wrong!",
            "Can't logout!",
            2,
            ""
        )
    return Returns.return_message("You are logged out!", "Redirecting to main page", 2, rLanding.index.route_path)

@AuthView.route(r.verify.route_path, methods=r.verify.http_types)
@Decorators.needs_to_be_guest
def verify(confirm_token):
    debug.print_v("on verify()")

    logic_resp = ViewAuthLogic.verify_confirm_code(confirm_token)
    if not logic_resp.success:
        return Returns.return_message(
            "Something went wrong!", logic_resp.content, 2, rLanding.index.route_path
        )
    return Returns.return_message(
        "Ok!", logic_resp.content, 2, r.index.route_path
    )


@AuthView.route(r.register.route_path, methods=r.register.http_types)
@Decorators.needs_to_be_guest
def register():
    debug.print_v("on register()")
    if request.method == 'GET':
        debug.print_v("Sending html page back (GET)")
        return render_template('webapp/auth/register.html')
    
    logic_resp = ViewAuthLogic.register(request.form)
    
    if not logic_resp.success:
        debug.print_e(logic_resp.content)
        return Returns.return_message(
            "Something went wrong!", logic_resp.content, 2,rAuth.index.route_path
        )
    return Returns.return_message(
        "Message", "You are registered. please activate your account via email!", 5, rAuth.index.route_path
    )
