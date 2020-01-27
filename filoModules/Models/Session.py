from filoModules.Models.User import User
class SessionEntries:
    logged_in = "logged_in"
    User = "User"


class Session(object):
    def __init__(self, logged_in, User: User):
        self.logged_in = logged_in
        self.User = User

    @classmethod
    def fromDict(cls, input_dict: dict):
        return cls(
            input_dict[SessionEntries.logged_in],
            User.fromDict(input_dict[SessionEntries.User])
        )

    @classmethod
    def fromSession(cls, input_session):
        if 'filo' not in input_session:
            return cls(None, None)
        return cls(
            input_session['filo'][SessionEntries.logged_in],
            User.fromDict(input_session['filo'][SessionEntries.User])
        )

    def toDict(self):
        return {
            SessionEntries.logged_in: self.logged_in if self.logged_in is not None else False,
            SessionEntries.User: self.User.toDict() if self.User is not None else None
        }
