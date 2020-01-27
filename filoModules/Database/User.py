from filoModules.Database.Handler import Handler as db_Handler
from filoModules.Models.User import UserEntries as m_UserEntries
from filoModules.Models.User import User as m_User
from filoModules.Models.LogicReturn import LogicReturn as m_LogicReturn


class User(db_Handler):  # method/constructor overloading: b
    def __init__(self):
        super().__init__("users")

    def update_user(self, User: m_User) -> m_LogicReturn:
        self.update_one(
            {
                m_UserEntries.user_uuid: User.user_uuid
            },
            {
                "$set": User.toDict()
            }
        )
        return m_LogicReturn.f_success_msg("Updated!")

    def get_user(self,
                 search_type: m_UserEntries,
                 query
                 ) -> m_LogicReturn:

        res = self.find_one(
            {
                search_type: query
            }
        )
        return m_LogicReturn.f_error_msg("User not found!") if res is None else m_LogicReturn.f_success("Found user!", m_User.fromDict(res))

    def get_all_users(self) -> m_LogicReturn:
        res = self.find_all()
        users = list()
        for fl in res:
            users.append(
                m_User.fromDict(fl)
            )

        return m_LogicReturn.f_success(f"Got {len(users)} users", users)

    def create_user(self, User: m_User) -> m_LogicReturn:
        return m_LogicReturn.f_error_msg("User already exists!") if self.__does_user_exist(User) else m_LogicReturn.f_success(True, self.insert_one(User.toDict()))

    def delete_user(self, User: m_User) -> m_LogicReturn:
        return m_LogicReturn.f_success(
            "Deleted user",
            self.delete_one(
                {
                    m_UserEntries.user_uuid: User.user_uuid
                }
            )
        )

    def __does_user_exist(self, User: m_User) -> bool:  # encapsulation, private fields
        res_1 = self.find_one(
            {
                m_UserEntries.email: User.email
            }
        )
        if res_1 is not None:
            return True
        return False
