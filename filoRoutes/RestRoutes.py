from filoModules.Models.Route import Route

prefix = "/api/rest"

light = Route.post(f"{prefix}/light")
light_front = Route.get(f"{prefix}/front/light/<string:device_uuid>")
change_state_front = Route.get(
    f"{prefix}/front/change_state/<string:device_uuid>/<string:state>")
get_state_front = Route.get(f"{prefix}/front/get_state/<string:device_uuid>")
unlock = Route.post(f"{prefix}/unlock")
lock = Route.post(f"{prefix}/lock")
unlock_fp = Route.post(f"{prefix}/unlock_fp")
lock_fp = Route.post(f"{prefix}/lock_fp")
events_update = Route.post(f"{prefix}/events/update")
events_get = Route.post(f"{prefix}/events/get")
index = Route.get(prefix)
findlock_get = Route.post(f"{prefix}/findlock/get")
findlock_update = Route.post(f"{prefix}/findlock/update")
get_name_by_uuid = Route.get(f"{prefix}/get_name/<string:i_uuid>")

get_last_location = Route.get(f"{prefix}/front/location/<string:device_uuid>")

routing_js = Route.get(f"{prefix}/routing.js")
