from filoModules.Models.Route import Route

# AuthView
prefix = "/admin"

findlocks = Route.get(f"{prefix}/findlocks")
findlock = Route.get(f"{prefix}/findlock/<string:fl_uuid>")
findlock_update = Route.post(f"{prefix}/findlock/<string:fl_uuid>/update")
findlock_delete = Route.get(f"{prefix}/findlock/<string:fl_uuid>/delete")
findlock_add_gps = Route.post(f"{prefix}/findlock/<string:fl_uuid>/add_gps")
users = Route.get(f"{prefix}/users")
user = Route.get(f"{prefix}/user/<string:u_uuid>")
user_delete = Route.get(f"{prefix}/user/<string:u_uuid>/delete")
user_update = Route.post(f"{prefix}/user/<string:u_uuid>/update")
user_send_mail = Route.post(f"{prefix}/user/<string:u_uuid>/send_mail")
index = Route.get(prefix)

wipe_col = Route.get(f"{prefix}/db_options/wipe/<string:col>")
db_options = Route.get(f"{prefix}/db_options")

logs = Route.get(f"{prefix}/logs")
view_logs = Route.get(f"{prefix}/view_logs")

def wipe_users():
    return str(wipe_col.route_path).replace("<string:col>", "users")
def wipe_findlocks():
    return str(wipe_col.route_path).replace("<string:col>", "findlocks")
def custom_findlock(fl_uuid):
    return str(findlock.route_path).replace("<string:fl_uuid>", fl_uuid)
def custom_findlock_update(fl_uuid):
    return str(findlock_update.route_path).replace("<string:fl_uuid>", fl_uuid)
def custom_findlock_delete(fl_uuid):
    return str(findlock_delete.route_path).replace("<string:fl_uuid>", fl_uuid)
def custom_findlock_add_gps(fl_uuid):
    return str(findlock_add_gps.route_path).replace("<string:fl_uuid>", fl_uuid)
def custom_user(u_uuid):
    return str(user.route_path).replace("<string:u_uuid>", u_uuid)
def custom_user_delete(u_uuid):
    return str(user_delete.route_path).replace("<string:u_uuid>", u_uuid)
def custom_user_update(u_uuid):
    return str(user_update.route_path).replace("<string:u_uuid>", u_uuid)
