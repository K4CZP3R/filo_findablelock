from filoModules.Database.Findlock import Findlock as db_Findlock
from filoModules.Database.User import User as db_User
from filoModules.Models.Findlock import FindlockEntries as m_FindlockEntries
from filoModules.Models.Findlock import Findlock as m_Findlock
from filoModules.Models.LogicReturn import LogicReturn as m_LogicReturn
from filoModules.Models.GpsLocation import GpsLocation as m_GpsLocation
from filoModules.Models.User import UserEntries as m_UserEntries
from filoModules.Models.User import User as m_User
from filoModules.Verifier import Verifier as v
from filoModules.Tools import Tools
from filoModules.Email import Email
import config, debug_data
import time

# TODO: Add debug


class ViewAdminLogic:
    @staticmethod
    def get_raw_logs() -> m_LogicReturn:
        return AdminLogic.get_raw_logs()
    @staticmethod
    def findlock_update(findlock_uuid, form_data) -> m_LogicReturn:
        if v.value_empty(findlock_uuid):
            return m_LogicReturn.f_error_msg("Data is missing")
        
        data_keys  = list()
        data_values = list()
        for i in form_data:
            data_keys.append(i)
            data_values.append(form_data[i])
        
        return AdminLogic.findlock_update(
            findlock_uuid, data_keys, data_values
        )
    @staticmethod
    def user_update(user_uuid, form_data) -> m_LogicReturn:
        if v.value_empty(user_uuid):
            return m_LogicReturn.f_error_msg("Data is missing")
        
        data_keys = list()
        data_values = list()
        for i in form_data:
            data_keys.append(i)
            data_values.append(form_data[i])
        
        return AdminLogic.user_update(
            user_uuid, data_keys, data_values
        )
    @staticmethod
    def findlock_delete(findlock_uuid) -> m_LogicReturn:
        if v.value_empty(findlock_uuid):
            return m_LogicReturn.f_error_msg("Data is missing!")
        return AdminLogic.remove_findlock(findlock_uuid)

    @staticmethod
    def user_send_mail(user_uuid, form_data) -> m_LogicReturn:
        subject = form_data.get("subjectInput", None)
        content = form_data.get("contentInput", None)

        if v.value_empty(user_uuid) \
            or v.value_empty(subject) \
                or v.value_empty(content):
            return m_LogicReturn.f_error_msg("Data is missing!")
        
        return AdminLogic.user_send_mail(
            user_uuid, subject, content
        )
        


    @staticmethod
    def add_gps_loc_to_findlock(findlock_uuid, form_data) -> m_LogicReturn:
        lat = form_data.get("latInput", None)
        lng = form_data.get("lngInput", None)
        if v.value_empty(findlock_uuid) or \
            v.value_empty(lat) or \
                v.value_empty(lng):
            return m_LogicReturn.f_error_msg("Data is missing!")

        return AdminLogic.add_gps_location_to_findlock(
            findlock_uuid,
            lat,
            lng
        )

    @staticmethod
    def user_delete(user_uuid) -> m_LogicReturn:
        if v.value_empty(user_uuid):
            return m_LogicReturn.f_error_msg("Data is missing!")

        return AdminLogic.remove_user(user_uuid)

    @staticmethod
    def get_list_of_users() -> m_LogicReturn:
        return AdminLogic.get_list_of_users()
    @staticmethod
    def get_list_of_user_entries() -> m_LogicReturn:
        return AdminLogic.get_list_of_user_entries()
    
    @staticmethod
    def get_user_info(user_uuid) -> m_LogicReturn:
        if v.value_empty(user_uuid):
            return m_LogicReturn.f_error_msg("Data is missing!")
        return AdminLogic.get_user_info(user_uuid)
    
    @staticmethod
    def get_user_entries() -> m_LogicReturn:
        return AdminLogic.get_all_user_entries()
    
    @staticmethod
    def get_findlock_info(findlock_uuid) -> m_LogicReturn:
        if v.value_empty(findlock_uuid):
            return m_LogicReturn.f_error_msg("Data is missing!")
        return AdminLogic.get_findlock_info(findlock_uuid)
    
    @staticmethod
    def get_findlock_entries() -> m_LogicReturn:
        return AdminLogic.get_all_findlock_entries()
    
    @staticmethod
    def wipe_collection(col_name) -> m_LogicReturn:
        if v.value_empty(col_name):
            return m_LogicReturn.f_error_msg("Data is missing!")
        return AdminLogic.wipe_collection(col_name)
        

class AdminLogic:
    @staticmethod
    def get_raw_logs() -> m_LogicReturn:
        filename = config.get_log_file_name()
        try:
            f = open(filename, 'r')
            lines = f.readlines()
            lines.reverse()
            out = ""
            for i in lines:
                out += f"{i}"
            f.close()
            return m_LogicReturn.f_success("Returned log file", out)
        except IOError:
            return m_LogicReturn.f_error_msg("Failed when reading file.")
    @staticmethod
    def wipe_collection(col_name) -> m_LogicReturn:
        valid_col_names = ["users", "findlocks"]

        if col_name not in valid_col_names:
            return m_LogicReturn.f_error_msg(f"{col_name} is not a valid col name!")
        
        if col_name == "users":
            db_User().drop_col()
            db_User().create_user(debug_data.get_dummy_user())
            db_User().create_user(debug_data.get_dummy_user_with_permissions())
        elif col_name == "findlocks":
            db_Findlock().drop_col()
            _findlock = debug_data.get_dummy_findlock()
            _findlock.FindlockPermission.master_uuid = debug_data.get_dummy_user().user_uuid
            _findlock.FindlockPermission.addAllowedUuid(debug_data.get_dummy_user_with_permissions().user_uuid)
            db_Findlock().create_findlock(_findlock)
        
        return m_LogicReturn.f_success_msg("Executed.")
        
    @staticmethod
    def user_send_mail(user_uuid, subject, content) -> m_LogicReturn:
        if not v.verify_uuid(user_uuid).success:
            return m_LogicReturn.f_error_msg(f"{user_uuid} is not a valid uuid")
        
        db_resp = db_User().get_user(
            m_UserEntries.user_uuid,
            user_uuid
        )
        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)
        
        _user = db_resp.addon_data
        _user: m_User

        _user_email = _user.email
        _user_voornaam = _user.first_name

        admin_mail = Email.get_admin_email(_user_email,_user_voornaam, subject, content)
        logic_resp = Email.send_email(_user_email, admin_mail)
        if not logic_resp.success:
            return m_LogicReturn.f_error_msg(logic_resp.content)
        return m_LogicReturn.f_success_msg("Mail sent!")

    @staticmethod
    def findlock_update(findlock_uuid, data_keys, data_values) -> m_LogicReturn:
        if not v.verify_uuid(findlock_uuid).success:
            return m_LogicReturn.f_error_msg(f"{findlock_uuid} is not a valid uuid")
        if len(data_keys) != len(data_values):
            return m_LogicReturn.f_error_msg("Mismatch in data!")

        for i in range(0, len(data_values)):
            data_val = data_values[i]
            if data_val == "None":
                data_values[i] = None
            elif data_val == "True":
                data_values[i] = True
            elif data_val == "False":
                data_values[i] = False
        
        valid_data_keys = Tools.get_types(m_FindlockEntries())

        db_resp = db_Findlock().get_findlock(
            m_FindlockEntries.device_uuid,
            findlock_uuid
        )
        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)
        
        _findlock = db_resp.addon_data
        _findlock: m_Findlock

        _findlock_dict = _findlock.toDict()

        for i in range(0, len(data_keys)):
            key = data_keys[i]
            if key not in valid_data_keys:
                return m_LogicReturn.f_error_msg(f"{key} is not a valid key!")
            val = data_values[i]

            _findlock_dict[key] = val
        
        _findlock = m_Findlock.fromDict(_findlock_dict)
        db_resp = db_Findlock().update_findlock(_findlock)
        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)
        return m_LogicReturn.f_success_msg(db_resp.content)

    @staticmethod
    def user_update(user_uuid, data_keys, data_values) -> m_LogicReturn:
        if not v.verify_uuid(user_uuid).success:
            return m_LogicReturn.f_error_msg(f"{user_uuid} is not a valid uuid")
        if len(data_keys) != len(data_values):
            return m_LogicReturn.f_error_msg("Mismatch in data!")

        for i in range(0, len(data_values)):
            data_val = data_values[i]
            if data_val == "None":
                data_values[i] = None
            elif data_val == "True":
                data_values[i] = True
            elif data_val == "False":
                data_values[i] = False
        
        valid_data_keys = Tools.get_types(m_UserEntries())

        db_resp = db_User().get_user(
            m_UserEntries.user_uuid,
            user_uuid
        )
        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)
        
        _user = db_resp.addon_data
        _user: m_User

        _user_dict = _user.toDict()

        for i in range(0, len(data_keys)):
            key = data_keys[i]
            if key not in valid_data_keys:
                return m_LogicReturn.f_error_msg(f"{key} is not a valid key!")
            val = data_values[i]

            _user_dict[key] = val
        
        _user = m_User.fromDict(_user_dict)
        db_resp = db_User().update_user(_user)
        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)
        return m_LogicReturn.f_success_msg(db_resp.content)

    
    @staticmethod
    def get_all_findlock_entries() -> m_LogicReturn:
        return m_LogicReturn.f_success(
            "Returned list of entries",
            Tools.get_types(m_FindlockEntries())
        )
    @staticmethod
    def get_findlock_info(findlock_uuid) -> m_LogicReturn:
        if not v.verify_uuid(findlock_uuid).success:
            return m_LogicReturn.f_error_msg(f"{findlock_uuid} is not a valid uuid")
        db_resp = db_Findlock().get_findlock(
            m_FindlockEntries.device_uuid,
            findlock_uuid
        )
        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)

        _findlock = db_resp.addon_data
        _findlock: m_Findlock
        
        return m_LogicReturn.f_success("Findlock found!", _findlock)

    @staticmethod
    def get_all_user_entries() -> m_LogicReturn:
        return m_LogicReturn.f_success(
            "Returned list of entries",
            Tools.get_types(m_UserEntries())
        )
    @staticmethod
    def get_user_info(user_uuid) -> m_LogicReturn:
        if not v.verify_uuid(user_uuid).success:
            return m_LogicReturn.f_error_msg(f"{user_uuid} is not a valid uuid")
        db_resp = db_User().get_user(
            m_UserEntries.user_uuid,
            user_uuid
        )
        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)

        _user = db_resp.addon_data
        _user: m_User
        
        return m_LogicReturn.f_success("User found!", _user)

    @staticmethod
    def add_gps_location_to_findlock(fl_uuid, lat, lng) -> m_LogicReturn:
        db_resp = db_Findlock().get_findlock(
            m_FindlockEntries.device_uuid,
            fl_uuid
        )
        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)

        _Findlock = db_resp.addon_data
        _Findlock: m_Findlock

        _new_gps_location = m_GpsLocation(lat, lng, str(Tools.get_unix_time()))

        _Findlock.GpsLocationHistory.add_location(_new_gps_location)

        db_Findlock().update_findlock(_Findlock)
        return m_LogicReturn.f_success_msg("ok!")

    @staticmethod
    def remove_findlock(findlock_uuid) -> m_LogicReturn:
        if not v.verify_uuid(findlock_uuid).success:
            return m_LogicReturn.f_error_msg("UUID is not valid!")
        db_resp = db_Findlock().get_findlock(
            m_FindlockEntries.device_uuid,
            findlock_uuid
        )
        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)

        _Findlock = db_resp.addon_data
        _Findlock: m_Findlock

        db_resp = db_Findlock().delete_findlock(
            _Findlock
        )
        if db_resp.success:
            return m_LogicReturn.f_success_msg(db_resp.content)
        return m_LogicReturn.f_error_msg(db_resp.content)

    @staticmethod
    def remove_user(u_uuid) -> m_LogicReturn:
        db_resp = db_User().get_user(
            m_UserEntries.user_uuid,
            u_uuid
        )
        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)

        _User = db_resp.addon_data
        _User: m_User

        db_resp = db_User().delete_user(
            _User
        )

        if db_resp.success:
            return m_LogicReturn.f_success_msg(db_resp.content)
        return m_LogicReturn.f_error_msg(db_resp.content)

    @staticmethod
    def get_list_of_findlocks() -> m_LogicReturn:
        db_resp = db_Findlock().get_all_findlocks()
        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)

        _Findlocks = db_resp.addon_data
        _Findlocks: [m_Findlock]
        return m_LogicReturn.f_success(f"List of {len(_Findlocks)} findlocks", _Findlocks)

    @staticmethod
    def get_list_of_users() -> m_LogicReturn:
        db_resp = db_User().get_all_users()
        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)

        _Users = db_resp.addon_data
        _Users: [m_User]
        return m_LogicReturn.f_success(f"List of {len(_Users)} users", _Users)

    @staticmethod
    def get_list_of_user_entries(only_editable=False) -> list:
        ignore_list = [
            m_UserEntries.password_hash,
            m_UserEntries.user_uuid,
            m_UserEntries.nfc_id,
            m_UserEntries.avatar_link,
            m_UserEntries.facebook_user_id,
            m_UserEntries.finger_id,
            m_UserEntries.google_user_id
        ]

        users_entries = list()

        for i in m_UserEntries.__dict__:
            if "__" not in i:
                if not only_editable or(only_editable and i not in ignore_list):
                    users_entries.append(
                        m_UserEntries.__dict__[i]
                    )
        return users_entries

    @staticmethod
    def get_list_of_findlock_entries(only_editable=False) -> list:
        ignore_list = [
            m_FindlockEntries.GpsLocationHistory,
            m_FindlockEntries.master_pincode,
            m_FindlockEntries.device_uuid,
            m_FindlockEntries.FindlockPermission,
            m_FindlockEntries.Event
        ]
        findlock_entries = list()
        for i in m_FindlockEntries.__dict__:
            if "__" not in i:
                if not only_editable or (only_editable and i not in ignore_list):
                    findlock_entries.append(
                        m_FindlockEntries.__dict__[i]
                    )
        return findlock_entries
