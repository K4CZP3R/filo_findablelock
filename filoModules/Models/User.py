import uuid

class UserEntries:
    first_name = "first_name"
    surname = "surname"
    email = "email"
    password_hash = "password_hash"
    phone_number = "phone_number"
    nfc_id = "nfc_id"
    finger_id = "finger_id"
    user_uuid = "user_uuid"
    google_user_id = "google_user_id"
    facebook_user_id = "facebook_user_id"
    avatar_link = "avatar_link"
    verified = "verified"
    friend_code = "friend_code"
    is_admin = "is_admin"


class User(object):  # objects/ classes
    def __init__(self, first_name, surname, email, password_hash, phone_number, nfc_id, finger_id, friend_code, user_uuid=str(uuid.uuid4()), google_user_id=None, avatar_link=None, facebook_user_id=None, verified=False, is_admin=False):  # constructors
        self.first_name = first_name
        self.surname = surname
        self.email = email
        self.password_hash = password_hash
        self.phone_number = phone_number
        self.nfc_id = nfc_id
        self.finger_id = finger_id
        self.user_uuid = user_uuid
        self.google_user_id = google_user_id
        self.avatar_link = avatar_link
        self.facebook_user_id = facebook_user_id
        self.verified = verified
        self.friend_code = friend_code
        self.is_admin = is_admin

    @classmethod
    def fromDict(cls, input_dict: dict):
        return cls(
            input_dict[UserEntries.first_name],
            input_dict[UserEntries.surname],
            input_dict[UserEntries.email],
            input_dict[UserEntries.password_hash],
            input_dict[UserEntries.phone_number],
            input_dict[UserEntries.nfc_id],
            input_dict[UserEntries.finger_id],
            input_dict[UserEntries.friend_code],
            user_uuid=input_dict[UserEntries.user_uuid],
            google_user_id=input_dict[UserEntries.google_user_id],
            avatar_link=input_dict[UserEntries.avatar_link],
            facebook_user_id=input_dict[UserEntries.facebook_user_id],
            verified=input_dict[UserEntries.verified],
            is_admin=input_dict[UserEntries.is_admin]

        )

    def toDict(self) -> dict:
        return {
            UserEntries.first_name: self.first_name,
            UserEntries.surname: self.surname,
            UserEntries.email: self.email,
            UserEntries.password_hash: self.password_hash,
            UserEntries.phone_number: self.phone_number,
            UserEntries.nfc_id: self.nfc_id,
            UserEntries.finger_id: self.finger_id,
            UserEntries.friend_code: self.friend_code,
            UserEntries.user_uuid: self.user_uuid,
            UserEntries.google_user_id: self.google_user_id,
            UserEntries.avatar_link: self.avatar_link,
            UserEntries.facebook_user_id: self.facebook_user_id,
            UserEntries.verified: self.verified,
            UserEntries.is_admin: self.is_admin
        }
