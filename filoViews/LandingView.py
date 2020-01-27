from flask import Blueprint, render_template, session, redirect, render_template
from filoModules.Debug import Debug
from filoRoutes import LandingRoutes as r
from filoRoutes import AuthRoutes as rAuth
from filoRoutes import AdminRoutes as rAdmin
import config


LandingView = Blueprint("LandingView", __name__)

debug = Debug("LandingView")


@LandingView.route(r.index.route_path)
def index():
    debug.print_v("on index()")
    debug.print_v(f"Version: {config.get_version()}")
    return render_template("webapp/index.html", config=config)
