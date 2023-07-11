from databases import Countings
from loader import db_session
from utils.mics import next_update_day

class CountingsService():
    def addCountings(self, user_id) -> Countings:
        if counting := self.getCountings(user_id):
            return counting
        counting = Countings(user_id=user_id)
        db_session.add(counting)
        db_session.commit()
        return counting

    def getUserCountings(self, user_id):
        return db_session.query(Countings.users, Countings)\
            .filter(Countings.user_id == str(user_id))\
                .first()

    def getCountings(self, user_id):
        return db_session.query(Countings)\
            .filter(Countings.user_id == str(user_id))\
                .first()

    def updateCounting(self, count_column, user_id, count_rating):
        updateCountings = {
            count_column : count_rating
        }
        db_session.query(Countings)\
            .filter(Countings.user_id == str(user_id))\
                .update(updateCountings, synchronize_session=False)
        db_session.commit()


    def resetCountings(self, 
        user_id, 
        count_rating = 0,
        mining_count = 0,
        count_present = 0
    ):
        updateCountings = {
            Countings.count_rating : count_rating,
            Countings.count_rating : mining_count,
            Countings.count_present : count_present,
            Countings.update_limit_date : next_update_day()
        }
        db_session.query(Countings)\
            .filter(Countings.user_id == str(user_id))\
                .update(updateCountings, synchronize_session=False)
        db_session.commit()

   