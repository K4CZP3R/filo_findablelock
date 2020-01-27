from filoModules.Models.Route import Route
# AuthView
prefix = "/auth"
index = Route.get_post(prefix)
logout = Route.get(f"{prefix}/logout")
register = Route.get_post(f"{prefix}/register")
google_verify = Route.get(f"{prefix}/google/verify")
google_login = Route.post(f"{prefix}/google_login")
facebook_verify = Route.post(f"{prefix}/facebook/verify")
facebook_login = Route.post(f"{prefix}/facebook_login")
verify = Route.get(f"{prefix}/verify/<string:confirm_token>")
