from filoModules.Models.Route import Route
prefix = "/user"

index = Route.get(prefix)
update = Route.get_post( f"{prefix}/update")
new_device = Route.get_post( f"{prefix}/new_device")
device = Route.get_post( f"{prefix}/device/<string:d_uuid>")
add_friend = Route.get_post( f"{prefix}/add_friend")


lock_unlock_screen = Route.get(f"{prefix}/device/<string:d_uuid>/lock_unlock")
light_screen = Route.get(f"{prefix}/device/<string:d_uuid>/light")
settings_screen = Route.get(f"{prefix}/settings")
fingerprints_screen = Route.get(f"{prefix}/device/<string:d_uuid>/fingerprints")

def custom_device(device_uuid):
    return str(device.route_path).replace("<string:d_uuid>", device_uuid)
def custom_lock_unlock_screen(device_uuid):
    return str(lock_unlock_screen.route_path).replace("<string:d_uuid>", device_uuid)
def custom_light_screen(device_uuid):
    return str(light_screen.route_path).replace("<string:d_uuid>", device_uuid)
def custom_fingerprints_screen(device_uuid):
    return str(fingerprints_screen.route_path).replace("<string:d_uuid>", device_uuid)