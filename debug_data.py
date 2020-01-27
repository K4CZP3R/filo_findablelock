from filoModules.Encryption import Encryption
from filoModules.Models.User import User as m_User
from filoModules.Models.Findlock import Findlock as m_Findlock
from filoModules.Models.FindlockPermission import FindlockPermission as m_FindlockPermission
from filoModules.Models.GpsLocationHistory import GpsLocationHistory as m_GpsLocationHistory
from filoModules.Models.GpsLocation import GpsLocation as m_GpsLocation
from filoModules.Models.Event import Event as m_Event

DUMMY_AVATAR_IMAGE = "https://www.clevelanddentalhc.com/wp-content/uploads/2018/03/sample-avatar-300x300.jpg"
DUMMY_USER = m_User(
    first_name="Kacper",
    surname="Serewis",
    email="kacper@findlock.site",
    password_hash=Encryption.encrypt_password("kak2tussen"),
    phone_number="+3185834573",
    nfc_id="31 5E 75 05",
    finger_id="1",
    friend_code="1337",
    user_uuid="00000000-0000-0000-0000-000000000000",
    avatar_link=DUMMY_AVATAR_IMAGE,
    verified=True,
    is_admin=True
)
DUMMY_USER_WITH_PERMISSIONS = m_User(
    first_name="Kamiel",
    surname="Wouters",
    email="kamiel@findlock.site",
    password_hash=Encryption.encrypt_password("12345678"),
    phone_number="112",
    nfc_id="11 2A F0 8C",
    finger_id="0",
    friend_code="2137",
    user_uuid="00000000-0000-0000-0000-000000000002",
    avatar_link=DUMMY_AVATAR_IMAGE,
    verified=True
)
DUMMY_FINDLOCK = m_Findlock(
    friendly_name="Sparta",
    GpsLocationHistory=m_GpsLocationHistory.empty(),
    master_pincode="1234",
    Event=m_Event.empty(),
    FindlockPermission=m_FindlockPermission.empty(),
    device_uuid="00000000-0000-0000-0000-000000000001"
)

DUMMY_LOCATION = m_GpsLocation("0","0", 0)

def get_dummy_user() -> m_User:
    return DUMMY_USER
def get_dummy_user_with_permissions() -> m_User:
    return DUMMY_USER_WITH_PERMISSIONS
def get_dummy_findlock() -> m_Findlock:
    return DUMMY_FINDLOCK
def get_dummy_location() -> m_GpsLocation:
    return DUMMY_LOCATION
    