
from filoModules.Database.Handler import Handler as db_Handler
from filoModules.Models.Findlock import Findlock as m_Findlock
from filoModules.Models.Findlock import FindlockEntries as m_FindlockEntries
from filoModules.Models.LogicReturn import LogicReturn as m_LogicReturn


class Findlock(db_Handler):
    def __init__(self):
        super().__init__("findlocks")

    def update_findlock(self, Findlock: m_Findlock)-> m_LogicReturn:
        self.update_one(
            {
                m_FindlockEntries.device_uuid: Findlock.device_uuid
            },
            {
                "$set": Findlock.toDict()
            }
        )
        return m_LogicReturn.f_success_msg("Findlock updated!")


    def get_findlock(self,
                     search_type: m_FindlockEntries,
                     query)-> m_LogicReturn:

        res = self.find_one({
            search_type: query
        })
        return m_LogicReturn.f_error_msg("Findlock not found") if res is None else m_LogicReturn.f_success("Found findlock!",m_Findlock.fromDict(res))
        
    def get_all_findlocks(self) -> m_LogicReturn:
        res = self.find_all()
        findlocks = list()
        for fl in res:
            findlocks.append(
                m_Findlock.fromDict(fl)
            )
        return m_LogicReturn.f_success(f"Found {len(findlocks)} findlocks.", findlocks)

    def create_findlock(self, Findlock: m_Findlock)-> m_LogicReturn:
        return m_LogicReturn.f_error_msg("This findlock already exists!") if self.__does_findlock_exist(Findlock) else m_LogicReturn.f_success("Findlock created!", self.insert_one(Findlock.toDict()))
        
    def delete_findlock(self, Findlock: m_Findlock) -> m_LogicReturn:
        return m_LogicReturn.f_success(
            "Findlock deleted!",
            self.delete_one({m_FindlockEntries.device_uuid: Findlock.device_uuid})
        )

    

    def __does_findlock_exist(self, Findlock: m_Findlock) -> bool:
        res = self.find_one({
            m_FindlockEntries.device_uuid: Findlock.device_uuid
        })
        return False if res is None else True
