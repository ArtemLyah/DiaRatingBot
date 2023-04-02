from databases.models import Users, UserGroup, UserRandom
from typing import Tuple
from services import UserService
from loader import db_session
from datetime import date

user_service = UserService()

class UserRandomService():
    def getUsersRandom(self, group_id) -> list[Tuple[Users, int, date]]:
        return db_session.query(Users, UserRandom.text_id, UserRandom.date_update)\
            .join(Users.userGroup)\
            .join(UserGroup.userRandom)\
                .filter(UserGroup.group_id == str(group_id))\
                    .all()

    def addUsers(self, group_id, users: list[Users], text_id: int):
        for user in users:
            user_group = user_service.getUserGroup(group_id, user.id)
            user_random = UserRandom(user_group_id = user_group.id, text_id = text_id)
            db_session.add(user_random)
        db_session.commit()
    
    def updateUsers(self, group_id, users: list[Users], text_id: int):
        db_session.query(UserRandom)\
            .filter(
                UserGroup.group_id == str(group_id)
            ).delete(synchronize_session=False)
                    
        self.addUsers(group_id, users, text_id)
