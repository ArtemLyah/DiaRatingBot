from databases import Groups
from loader import db_session

class GroupService():
    def getGroup(self, telegram_id) -> Groups:
        return db_session.query(Groups).filter(Groups.id == str(telegram_id)).first()

    def addGroup(self, telegram_id, fullname):
        if group := self.getGroup(telegram_id):
            return group
        group = Groups(id=str(telegram_id), fullname=fullname)
        db_session.add(group)
        db_session.commit()
        return group