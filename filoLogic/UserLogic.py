from filoModules.Database.Findlock import Findlock as DbFindlock
from filoModules.Database.User import User as DbUser
from filoLogic.SessionLogic import SessionLogic
from filoLogic.AdminLogic import AdminLogic
from filoModules.Models.LogicReturn import LogicReturn as m_LogicReturn
from filoModules.Models.Findlock import FindlockEntries as m_FindlockEntries
from filoModules.Models.Findlock import Findlock as m_Findlock
from filoModules.Models.Session import Session as m_Session
from filoModules.Models.User import User as m_User
from filoModules.Models.User import UserEntries as m_UserEntries
from filoModules.Verifier import Verifier as v
from flask import session
default_device_uuid = "00000000-0000-0000-0000-000000000001"
class ViewUserLogic:
    @staticmethod
    def add_friend(_session: m_Session, form_data) -> m_LogicReturn:
        print(form_data)
        friend_code = form_data.get("friendCode", None)
        device_uuid = form_data.get("device_uuid", default_device_uuid) #doet pijn maar moet wel

        if v.value_empty(friend_code) \
            or v.value_empty(device_uuid):
            return m_LogicReturn.f_error_msg("Data is missing!")
        if type(_session) != m_Session:
            return m_LogicReturn.f_error_msg("Session is not a valid type!")
        
        _user_uuid = _session.User.user_uuid
        return UserLogic.add_friend(
            _user_uuid, device_uuid, friend_code
        )
    
    @staticmethod
    def user_data_is_missing(_session: m_Session) -> m_LogicReturn:
        if v.value_empty(_session):
            return m_LogicReturn.f_error_msg("Data is missing!")
        if type(_session) != m_Session:
            return m_LogicReturn.f_error_msg("Session is not a valid type!")
        _user_dict = _session.User.toDict()
        return UserLogic.user_data_missing(_user_dict)
    
    @staticmethod
    def get_user_findlocks(_session: m_Session) -> m_LogicReturn:
        if v.value_empty(_session):
            return m_LogicReturn.f_error_msg("Data is missing!")
        if type(_session) != m_Session:
            return m_LogicReturn.f_error_msg("Session is not a valid type!")
        
        _user_uuid = _session.User.user_uuid
        return UserLogic.get_user_findlocks(_user_uuid, master_only=False)
    
    @staticmethod
    def update_user_data(_session: m_Session,form_data) -> m_LogicReturn:
        if v.value_empty(_session):
            return m_LogicReturn.f_error_msg("Data is missing")
        
        if type(_session) != m_Session:
            return m_LogicReturn.f_error_msg("Session is not a valid type!")
        
        _user_dict = _session.User.toDict()
        return UserLogic.update_user_data(
            _user_dict, form_data
        )
    
    @staticmethod
    def pair_with_findlock(_session: m_Session, form_data) -> m_LogicReturn:        
        uuidInput = form_data.get("uuidInput", None)
        pincodeInput = form_data.get("pincodeInput", None)

        if v.value_empty(_session) \
            or v.value_empty(uuidInput) \
                or v.value_empty(pincodeInput):
            return m_LogicReturn.f_error_msg("Data is missing")
        
        _user_uuid = _session.User.user_uuid
        return UserLogic.pair_with_findlock(
            uuidInput, pincodeInput, _user_uuid
        )

    @staticmethod
    def user_allowed_to_use_findlock(_session: m_Session, device_uuid) -> m_LogicReturn:
        if v.value_empty(_session) \
            or v.value_empty(device_uuid):
                return m_LogicReturn.f_error_msg("Data is missing!")
        
        _user_uuid = _session.User.user_uuid
        return UserLogic.check_if_user_allowed_to_use_findlock(
            _user_uuid, device_uuid, _master_only=False
        )
    
    @staticmethod
    def get_findlock_info(d_uuid) -> m_LogicReturn:
        if v.value_empty(d_uuid):
            return m_LogicReturn.f_error_msg("Data is missing!")
        return UserLogic.get_info_about_findlock(d_uuid)

    @staticmethod
    def get_allowed_users_for_findlock(_findlock_uuid) -> m_LogicReturn:
        if v.value_empty(_findlock_uuid):
            return m_LogicReturn.f_error_msg("Data is missing")
        return UserLogic.get_allowed_users_for_findlock(_findlock_uuid)

    
class UserLogic:
    @staticmethod
    def get_allowed_users_for_findlock(_findlock_uuid) -> m_LogicReturn:
        if not v.verify_uuid(_findlock_uuid).success:
            return m_LogicReturn.f_error_msg(f"{_findlock_uuid} is not a valid uuid!")
        
        db_resp = DbFindlock().get_findlock(
            m_FindlockEntries.device_uuid,
            _findlock_uuid
        )
        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)
        
        findlock = db_resp.addon_data
        findlock: m_Findlock

        allowed_names = list()
        for u in findlock.FindlockPermission.allowed_uuids:
            db_resp = DbUser().get_user(
                m_UserEntries.user_uuid,
                u
            )
            if not db_resp.success:
                return m_LogicReturn.f_error_msg(db_resp.content)
            
            tmp_user = db_resp.addon_data
            tmp_user: m_User

            allowed_names.append(f"{tmp_user.first_name} {tmp_user.surname}")
        
        return m_LogicReturn.f_success("Ok!", allowed_names)
    @staticmethod
    def add_friend(_user_uuid ,_findlock_uuid, _friendcode) -> m_LogicReturn: #using
        if not v.verify_uuid(_findlock_uuid).success:
            return m_LogicReturn.f_error_msg(f"{_findlock_uuid} is not a valid uuid!")
        if not v.verify_uuid(_user_uuid).success:
            return m_LogicReturn.f_error_msg(f"{_user_uuid} is not a valid uuid!")

        logic_resp = UserLogic.check_if_user_allowed_to_use_findlock(_user_uuid,_findlock_uuid)
        if not logic_resp.success:
            return m_LogicReturn.f_error_msg( logic_resp.content)
        
        if not v.verify_friendcode(_friendcode).success:
            return m_LogicReturn.f_error_msg(f"{_friendcode} is not a valid friendcode")
        
        friendcode_splitter = str(_friendcode).split("#")
        voornaam = friendcode_splitter[0]
        friendcode = friendcode_splitter[1]

        users_of_friendcode = DbUser().get_all_users()
        if not users_of_friendcode.success:
            return m_LogicReturn.f_error_msg( users_of_friendcode.content)
        
        users_of_friendcode = users_of_friendcode.addon_data


        user_of_friendcode = None
        for u in users_of_friendcode:
            _voornaam = u.first_name 
            _friendcode = u.friend_code

            if _voornaam == voornaam and _friendcode == friendcode:
                user_of_friendcode = u
        
        if v.value_empty(user_of_friendcode):
            return m_LogicReturn.f_error_msg( "Could not find user by this friendcode!")
        
        user_of_friendcode: m_User
            


        db_resp = DbFindlock().get_findlock(
            m_FindlockEntries.device_uuid,
            _findlock_uuid
        )
        if not db_resp.success:
            return m_LogicReturn.f_error_msg( "Could not get findlock with this uuid!")
        
        Findlock = db_resp.addon_data
        Findlock: m_Findlock

        if user_of_friendcode.user_uuid in Findlock.FindlockPermission.allowed_uuids:
            return m_LogicReturn.f_error_msg( "This user already have permissions")
        
        Findlock.FindlockPermission.addAllowedUuid(user_of_friendcode.user_uuid)

        db_resp = DbFindlock().update_findlock(Findlock)
        if not db_resp.success:
            return m_LogicReturn.f_error_msg( db_resp.content)
        return m_LogicReturn.f_success_msg(f"{friendcode} is added!")
   
    @staticmethod
    def get_info_about_findlock(device_uuid) -> m_LogicReturn:
        if not v.verify_uuid(device_uuid).success:
            return m_LogicReturn.f_error_msg(f"{device_uuid} is not a valid uuid!")
        db_resp = DbFindlock().get_findlock(
            m_FindlockEntries.device_uuid,
            device_uuid
        )
        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.addon_data)

        Findlock = db_resp.addon_data
        Findlock: m_Findlock

        return m_LogicReturn.f_success("Found info!", Findlock)

    @staticmethod
    def check_if_user_allowed_to_use_findlock(_user_uuid,_findlock_uuid, _master_only=True) -> m_LogicReturn: #using
        if not v.verify_uuid(_user_uuid).success:
            return m_LogicReturn.f_error_msg(f"{_user_uuid} is not a valid uuid")
        db_resp = DbFindlock().get_findlock(
            m_FindlockEntries.device_uuid,
            _findlock_uuid
        )
        if not db_resp.success:
            return m_LogicReturn.f_error_msg( db_resp.content)

        Findlock = db_resp.addon_data
        Findlock: m_Findlock

        if _user_uuid == Findlock.FindlockPermission.master_uuid:
            return m_LogicReturn.f_success_msg( "User is master")

        if not _master_only:
            if _user_uuid in Findlock.FindlockPermission.allowed_uuids:
                return m_LogicReturn.f_success_msg( "User is allowed!")
        return m_LogicReturn.f_error_msg( "User is not allowed!")

    @staticmethod
    def get_user_findlocks(_user_uuid: str,master_only=True) -> m_LogicReturn: #using
        if not v.verify_uuid(_user_uuid).success:
            return m_LogicReturn.f_error_msg(f"{_user_uuid} is not a valid uuid")
        
        # todo: make query with find (and not find_one)
        db_resp = DbFindlock().get_all_findlocks()
        if not db_resp.success:
            return m_LogicReturn.f_error_msg( db_resp.content)
        
        Findlocks = db_resp.addon_data
        Findlocks: [m_Findlock]

        findlocks_list = list()
        for i in Findlocks:
            i: m_Findlock
            if i.FindlockPermission.master_uuid == _user_uuid:
                findlocks_list.append(i)
        if not master_only:
            for i in Findlocks:
                i: m_Findlock
                if _user_uuid in i.FindlockPermission.allowed_uuids:
                    findlocks_list.append(i)
        return m_LogicReturn.f_success("Found findlocks", findlocks_list)

    @staticmethod
    def pair_with_findlock(_device_uuid, _device_pincode, _user_uuid) -> m_LogicReturn: #using    
        if not v.verify_uuid(_device_uuid).success:
            return m_LogicReturn.f_error_msg(f"{_device_uuid} is not a valid uuid!")
        
        db_resp = DbFindlock().get_findlock(
            m_FindlockEntries.device_uuid,
            _device_uuid
        )
        if not db_resp.success:
            return m_LogicReturn.f_error_msg( "This uuid does not exist!")
        Findlock = db_resp.addon_data
        Findlock: m_Findlock

        if Findlock.FindlockPermission.master_uuid is not None:
            return m_LogicReturn.f_error_msg( "This findlock is already paired!")

        if Findlock.master_pincode != _device_pincode:
            return m_LogicReturn.f_error_msg( "Pincode mismatch!")

        Findlock.FindlockPermission.master_uuid = _user_uuid

        db_resp = DbFindlock().update_findlock(Findlock)
        if not db_resp.success:
            return m_LogicReturn.f_error_msg( db_resp.content)
        return m_LogicReturn.f_success_msg( "Paired!")

    @staticmethod
    def update_user_data(_user_dict: dict,form_data) -> m_LogicReturn: #using
        if type(_user_dict) != dict:
            return m_LogicReturn.f_error_msg("Session type is invalid")
        
        logic_resp = UserLogic.user_data_missing(_user_dict)
        if not logic_resp.success:
            return m_LogicReturn.f_error_msg(logic_resp.content)
        missing_list = logic_resp.addon_data

        for i in missing_list:
            form_entry = form_data.get(f"{i}Input", None)
            if form_entry is not None and len(form_entry) > 0:
                _user_dict[i] = form_entry

        new_user = m_User.fromDict(_user_dict)
        db_resp = DbUser().update_user(new_user)

        if not db_resp.success:
            return m_LogicReturn.f_error_msg( db_resp.content)
        if not SessionLogic.update_session_using_db().success:
            return m_LogicReturn.f_error_msg( "Updating session gaat fout!")
        return m_LogicReturn.f_success_msg("Updated user data!")

    @staticmethod
    def user_data_missing(_user_dict: dict) -> m_LogicReturn: #using
        if type(_user_dict) != dict:
            return m_LogicReturn.f_error_msg("User is not in a dict format")
        
        editable_user_entries = AdminLogic.get_list_of_user_entries(
            only_editable=True)
        
        
        missing_entries = list()
        for i in editable_user_entries:
            if _user_dict[i] is None:
                missing_entries.append(i)

        if len(missing_entries) > 0:
            return m_LogicReturn.f_success(
                "Your account misses some data!",
                missing_entries
            )

        return m_LogicReturn.f_error_msg("All data is filled, no action needed!")