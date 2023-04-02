from databases.models import Users, UserGroup, Countings
from loader import db_session
from sqlalchemy.sql import and_
from typing import Union

class UserService():
    def addUser(self, telegram_id, full_name, username) -> Union[Users, Countings]:
        if user := self.getUser(telegram_id):
            return user
        user = Users(id=str(telegram_id), full_name=full_name, username=username)
        db_session.add(user)
        db_session.commit()
        return user
    
    def getUser(self, user_id) -> Users:
        return db_session.query(Users)\
            .filter(Users.id == str(user_id))\
                .first()

    def getAllUsersInGroup(self, group_id) -> list[Users]:
        return db_session.query(Users)\
            .join(UserGroup)\
                .filter(UserGroup.group_id == str(group_id))\
                    .group_by(Users)\
                        .all()

    def addUserGroup(self, group_telegram_id, user_telegram_id) -> UserGroup:
        if user_group := self.getUserGroup(group_telegram_id, user_telegram_id):
            return user_group
        user_group = UserGroup(user_id=user_telegram_id, group_id=group_telegram_id)
        db_session.add(user_group)
        db_session.commit()
        return user_group

    def getUserGroup(self, group_telegram_id, user_telegram_id) -> UserGroup:
        return db_session.query(UserGroup).filter(
            and_(
                UserGroup.user_id==str(user_telegram_id),
                UserGroup.group_id==str(group_telegram_id)
            )
        ).first()
    
    def getUserByUsername(self, username) -> Users:
        return db_session.query(Users).filter(Users.username == username).first()
    
    def setBan(self, group_id, user_id, isban):
        updateUserGroup = {
            UserGroup.is_ban : isban
        }        
        db_session.query(UserGroup)\
            .filter(
                and_(
                    UserGroup.user_id == str(user_id),
                    UserGroup.group_id == str(group_id)
                )
            ).update(updateUserGroup, synchronize_session=False)
        db_session.commit()