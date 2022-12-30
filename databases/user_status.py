class Rating():
    def __init__(self, db) -> None:
        self.db = db
        
    def get_rating(self, group_id, user_id):
        sql_select_rating = f"SELECT rating FROM users_status WHERE user_id='{user_id}' AND group_id='{group_id}'"
        rating = self.db.connector.execute(sql_select_rating).fetchone()
        return rating[0] if rating else None

    def set_rating(self, group_id, user_id, increase_rating):
        new_rating = self.get_rating(group_id, user_id)+increase_rating
        sql_update_rating = f"UPDATE users_status SET rating={new_rating} WHERE user_id='{user_id}' AND group_id='{group_id}'"
        self.db.connector.execute(sql_update_rating)
        return new_rating

class IsBan():
    def __init__(self, db) -> None:
        self.db = db

    def get_ban(self, group_id, user_id):
        sql_select_ban = f"SELECT is_ban FROM users_status WHERE user_id='{user_id}' AND group_id='{group_id}'"
        isban = self.db.connector.execute(sql_select_ban).fetchone()
        return isban[0] if isban else None

    def set_ban(self, group_id, user_id, is_ban):
        sql_update_ban = f"UPDATE users_status SET is_ban={is_ban} WHERE user_id='{user_id}' AND group_id='{group_id}'"
        self.db.connector.execute(sql_update_ban)

