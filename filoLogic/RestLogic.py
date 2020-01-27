
import json
import time
from filoModules.Database.Findlock import Findlock as db_Findlock
from filoModules.Database.User import User as db_User
from filoModules.Models.Findlock import Findlock as m_Findlock
from filoModules.Models.LogicReturn import LogicReturn as m_LogicReturn
from filoModules.Models.Findlock import FindlockEntries as m_FindlockEntries
from filoModules.Models.GpsLocation import GpsLocation as m_GpsLocation
from filoModules.Models.User import User as m_User
from filoModules.Models.User import UserEntries as m_UserEntries
from filoModules.Models.Findlock import Findlock as m_Findlock
from filoModules.Verifier import Verifier as v

from filoModules.Models.Event import EventTypes as m_EventTypes
from filoModules.Models.Event import Event as m_Event
from filoModules.Tools import Tools as t
from filoModules.Models.Findlock import FindlockUpdateTypes as m_FindlockUpdateTypes

class ViewRestLogic:
    @staticmethod
    def get_findlock_location(device_uuid) -> m_LogicReturn:
        if v.value_empty(device_uuid):
            return m_LogicReturn.f_error_msg("Data is missing!")
        return RestLogic.get_findlock_location(device_uuid)
    @staticmethod
    def get_name_by_uuid(input_uuid) -> m_LogicReturn:
        if v.value_empty(input_uuid):
            return m_LogicReturn.f_error_msg("Data is missing!")
        return RestLogic.get_name_by_uuid(input_uuid)
    
    @staticmethod
    def light_findlock_frontend(device_uuid) -> m_LogicReturn:
        if v.value_empty(device_uuid):
            return m_LogicReturn.f_error_msg("Data is missing!")
        return RestLogic.set_findlock_event(
            device_uuid,
            m_EventTypes.light
        )
        
    @staticmethod
    def light_findlock(form_data) -> m_LogicReturn:
        device_uuid = form_data.get('device_uuid', None)
        if v.value_empty(device_uuid):
            return m_LogicReturn.f_error_msg("Data is missing!")

        return RestLogic.set_findlock_event(
            device_uuid,
            m_EventTypes.light
        )
    
    @staticmethod
    def change_findlock_state_frontend(device_uuid, state) -> m_LogicReturn:
        if v.value_empty(device_uuid) \
            or v.value_empty(state):
                return m_LogicReturn.f_error_msg("Data is missing!")
        
        return RestLogic.set_findlock_event(
            device_uuid,
            state
        )

    @staticmethod
    def get_findlock_state_frontend(device_uuid) -> m_LogicReturn:
        if v.value_empty(device_uuid):
            return m_LogicReturn.f_error_msg("Data is missing!")
        return RestLogic.get_findlock_event(device_uuid)
        
    @staticmethod
    def unlock_findlock_nfc(form_data) -> m_LogicReturn:
        device_uuid = form_data.get('device_uuid', None)
        detected_nfc = form_data.get('detected_nfc', None)
        if v.value_empty(device_uuid) \
            or v.value_empty(detected_nfc):
            return m_LogicReturn.f_error_msg("Data is missing!")
        
        return RestLogic.set_findlock_lock_state(
            device_uuid,
            m_EventTypes.unlock,
            detected_nfc,
            m_UserEntries.nfc_id
        )
        
    @staticmethod
    def lock_findlock_nfc(form_data) -> m_LogicReturn:
        device_uuid = form_data.get('device_uuid', None)
        detected_nfc = form_data.get('detected_nfc', None)
        if v.value_empty(device_uuid) \
            or v.value_empty(detected_nfc):
            return m_LogicReturn.f_error_msg("Data is missing!")
        
        return RestLogic.set_findlock_lock_state(
            device_uuid,
            m_EventTypes.lock,
            detected_nfc,
            m_UserEntries.nfc_id
        )
        
    
    @staticmethod
    def unlock_findlock_fingerprint(form_data) -> m_LogicReturn:
        device_uuid = form_data.get('device_uuid', None)
        detected_fp = form_data.get('detected_fp', None)
        if v.value_empty(device_uuid) \
            or v.value_empty(detected_fp):
            return m_LogicReturn.f_error_msg("Data is missing!")
        
        return RestLogic.set_findlock_lock_state(
            device_uuid,
            m_EventTypes.unlock,
            detected_fp,
            m_UserEntries.finger_id
        )
    
    @staticmethod
    def lock_findlock_fingerprint(form_data) -> m_LogicReturn:
        device_uuid = form_data.get('device_uuid', None)
        detected_fp = form_data.get('detected_fp', None)
        if v.value_empty(device_uuid) \
            or v.value_empty(detected_fp):
            return m_LogicReturn.f_error_msg("Data is missing!")
        
        return RestLogic.set_findlock_lock_state(
            device_uuid,
            m_EventTypes.lock,
            detected_fp,
            m_UserEntries.finger_id
        )

    @staticmethod
    def update_findlock_event(form_data) -> m_LogicReturn:
        device_uuid = form_data.get('device_uuid', None)
        executed = form_data.get('executed', None)
        if v.value_empty(device_uuid) \
            or v.value_empty(executed):
            return m_LogicReturn.f_error_msg("Data is missing!")
        
        if type(executed) == int:
            executed = True if executed == 1 else False
        elif type(executed) == str:
            executed = True if str(executed).lower() == "true" else False
        else:
            return m_LogicReturn.f_error_msg("Unknown type of executed!")

        return RestLogic.update_findlock_event(
            device_uuid,
            executed
        )
        
    @staticmethod
    def get_findlock_event(form_data) -> m_LogicReturn:
        device_uuid = form_data.get('device_uuid', None)
        if v.value_empty(device_uuid):
            return m_LogicReturn.f_error_msg("Data is missing!")
        return RestLogic.get_findlock_event(device_uuid)
        
    @staticmethod
    def get_findlock(form_data) -> m_LogicReturn:
        device_uuid = form_data.get('device_uuid', None)
        if v.value_empty(device_uuid):
            return m_LogicReturn.f_error_msg("Data is missing!")
        
        return RestLogic.get_findlock(
            device_uuid
        )
    
    @staticmethod
    def update_findlock(form_data) -> m_LogicReturn:
        device_uuid = form_data.get('device_uuid', None)
        update_type = form_data.get('update_type', None)
        update_data = form_data.get('update_data', None)

        if v.value_empty(device_uuid) \
            or v.value_empty(update_type) \
                or v.value_empty(update_data):
                return m_LogicReturn.f_error_msg("Data is missing")
        


        return RestLogic.update_findlock(
            device_uuid,
            update_type,
            update_data
        )
        
    
    
        
    

        
        
class RestLogic:
    @staticmethod
    def get_findlock_location(device_uuid) -> m_LogicReturn:
        if not v.verify_uuid(device_uuid).success:
            return m_LogicReturn.f_error_msg("Invalid UUID")
        
        db_resp = db_Findlock().get_findlock(
            m_FindlockEntries.device_uuid, device_uuid
        )
        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)
        
        findlock = db_resp.addon_data
        findlock: m_Findlock

        n_locations = findlock.GpsLocationHistory.get_location_count()-1
        if n_locations < 0:
            return m_LogicReturn.f_error_msg("No locations")
        return m_LogicReturn.f_success("Returned.", findlock.GpsLocationHistory.get_location(n_locations).toDict())

    @staticmethod
    def get_name_by_uuid(i_uuid) -> m_LogicReturn: #using
        if not v.verify_uuid(i_uuid).success:
            return m_LogicReturn.f_error_msg("Invalid UUID")
        
        db_resp = db_User().get_user(
            m_UserEntries.user_uuid, i_uuid
        )
        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)

        User = db_resp.addon_data
        User: m_User
        return m_LogicReturn.f_success_msg(f"{User.first_name} {User.surname}")

    @staticmethod
    def get_findlock(device_uuid) -> m_LogicReturn:
        if v.value_empty(device_uuid):
            return m_LogicReturn.f_error_msg("post data is missing")

        db_resp = db_Findlock().get_findlock(
            m_FindlockEntries.device_uuid,
            device_uuid
        )

        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)

        Findlock = db_resp.addon_data
        Findlock: m_Findlock

        return m_LogicReturn.f_success_msg(Findlock.toDict())

    @staticmethod
    def update_findlock(device_uuid, update_type, update_data) -> m_LogicReturn:
        if v.value_empty(device_uuid) \
            or v.value_empty(update_data) \
                or v.value_empty(update_type):
            return m_LogicReturn.f_error_msg("post data is missing!")
        

        db_resp = db_Findlock().get_findlock(
            m_FindlockEntries.device_uuid,
            device_uuid
        )

        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)

        Findlock = db_resp.addon_data
        Findlock: m_Findlock

        valid_update_types = t.get_types(m_FindlockUpdateTypes())
        if update_type not in valid_update_types:
            return m_LogicReturn.f_error_msg("Unsupported update type!")
        
        if update_type == m_FindlockUpdateTypes.gps_location:
            try:
                update_data = json.loads(update_data)
                update_data = m_GpsLocation.fromDict(update_data)
            except:
                return m_LogicReturn.f_error_msg("Update data is malformed!")

        if update_type == m_FindlockUpdateTypes.gps_location:
            Findlock.GpsLocationHistory.add_location(update_data)
        else:
            return m_LogicReturn.f_error_msg("this update type is not implemented...")

        db_resp = db_Findlock().update_findlock(Findlock)
        return m_LogicReturn.f_success_msg("Findlock updated!")

    @staticmethod
    def update_findlock_event(device_uuid, executed:bool) -> m_LogicReturn:

        db_resp = db_Findlock().get_findlock(
            m_FindlockEntries.device_uuid,
            device_uuid
        )

        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)

        Findlock = db_resp.addon_data
        Findlock: m_Findlock

        Findlock.Event.executed = executed
        db_Findlock().update_findlock(Findlock)
        return m_LogicReturn.f_success_msg("updated!")

    @staticmethod
    def get_findlock_event(device_uuid) -> m_LogicReturn: #using
        if not v.verify_uuid(device_uuid).success:
            return m_LogicReturn.f_error_msg(f"{device_uuid} is not a valid uuid")
        
        db_resp = db_Findlock().get_findlock(
            m_FindlockEntries.device_uuid,
            device_uuid
        )
        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)

        Findlock = db_resp.addon_data
        Findlock: m_Findlock

        # TODO: check if client waits for data in data and not in content
        return m_LogicReturn.f_success("Found event.", Findlock.Event.toDict())

    @staticmethod
    def set_findlock_event(device_uuid, event_type) -> m_LogicReturn: #using
        valid_event_types = t.get_types(m_EventTypes())
        print(valid_event_types)
        if event_type not in valid_event_types:
            return m_LogicReturn.f_error_msg(f"{event_type} is not a valid event type!")
        
        if not v.verify_uuid(device_uuid).success:
            return m_LogicReturn.f_error_msg(f"{device_uuid} is not a valid uuid")
        
        db_resp = db_Findlock().get_findlock(
            m_FindlockEntries.device_uuid,
            device_uuid
        )
        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)        
        _findlock = db_resp.addon_data
        _findlock: m_Findlock

        _findlock.Event = m_Event(event_type, t.get_unix_time())

        db_resp = db_Findlock().update_findlock(_findlock)
        return m_LogicReturn.f_success_msg("Event updated!")


    

    @staticmethod
    def set_findlock_lock_state( #using
        device_uuid,
        new_lock_state, #mEventType
        auth_value, #
        auth_type): #userentries


        if not v.verify_uuid(device_uuid).success:
            return m_LogicReturn.f_error_msg(f"{device_uuid} is not a valid uuid!")
        
        event_types = t.get_types(m_EventTypes())
        if new_lock_state not in event_types:
            return m_LogicReturn.f_error_msg(f"{new_lock_state} is not a valid event type!")
        
        auth_types = t.get_types(m_UserEntries())
        if auth_type not in auth_types:
            return m_LogicReturn.f_error_msg(f"{auth_type} is not a valid userentry!")
        

        db_resp = db_Findlock().get_findlock(
            m_FindlockEntries.device_uuid,
            device_uuid
        )
        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)
        
        _findlock = db_resp.addon_data
        _findlock: m_Findlock

        db_resp = db_User().get_all_users()
        if not db_resp.success:
            return m_LogicReturn.f_error_msg(db_resp.content)
        
        _users = db_resp.addon_data
        user_have_rights = False

        if auth_type == m_UserEntries.finger_id:
            for user in _users:
                if user.finger_id == auth_value:
                    if user.user_uuid == _findlock.FindlockPermission.master_uuid:
                        user_have_rights = True
                    if user.user_uuid in _findlock.FindlockPermission.allowed_uuids:
                        user_have_rights = True
        elif auth_type == m_UserEntries.nfc_id:
            for user in _users:
                if user.nfc_id == auth_value:
                    if user.user_uuid == _findlock.FindlockPermission.master_uuid:
                        user_have_rights = True
                    if user.user_uuid in _findlock.FindlockPermission.allowed_uuids:
                        user_have_rights = True
        else:
            return m_LogicReturn.f_error_msg("Unsupported auth type!")
        

        if not user_have_rights:
            return m_LogicReturn.f_error_msg("Permission error!")
        
        return RestLogic.set_findlock_event(
            device_uuid, new_lock_state
        )





