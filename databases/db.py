import sqlalchemy as sa
from config import database_settings

class User():
    def __init__(self, db) -> None:
        self.db = db
    def get_info(self, id):
        sql = f"SELECT id, username, fullname FROM users_info WHERE id='{id}'"
        return self.db.connector.execute(sql).fetchone()
    def add(self, group_id, user_id, username, fullname):
        sql_user_info = f"INSERT INTO users_info(id, username, fullname) VALUES('{user_id}', '{username}', '{fullname}')"
        self.db.connector.execute(sql_user_info)
        sql_relations = f"INSERT INTO users_rating(user_id, group_id) VALUES('{user_id}', '{group_id}')"
        self.db.connector.execute(sql_relations)
        self.db.connector.commit()
    def remove_rating(self, user_id, group_id):
        sql_delete = f"DELETE FROM users_rating WHERE user_id = '{user_id}' AND group_id='{group_id}'"
        self.db.connector.execute(sql_delete)
        self.db.connector.commit()

class Group():
    def __init__(self, db) -> None:
        self.db = db
    def get_info(self, id):
        sql = f"SELECT * FROM groups_info WHERE id='{id}'"
        return self.db.connector.execute(sql).fetchone()
    def add(self, user_id, username, name):
        if not self.get_info(user_id):
            sql_group_info = f"INSERT INTO groups_info(id, username, name) VALUES('{user_id}', '{username}', '{name}')"
            self.db.connector.execute(sql_group_info)
            self.db.connector.commit()

class Sticker():
    def __init__(self, db) -> None:
        self.db = db
    def get_rate(self, unique_file_id):
        sql = f"SELECT rate FROM sticker_info WHERE unique_file_id='{unique_file_id}'"
        return self.db.connector.execute(sql).fetchone()
    def add_rate(self, unique_file_id, rate):
        sql_sticker_info = f"INSERT INTO sticker_info(unique_file_id, rate) VALUES('{unique_file_id}', {rate})"
        self.db.connector.execute(sql_sticker_info)
        self.db.connector.commit()
        
class Database():
    def __init__(self) -> None:
        self.db_settings = database_settings
        self.url = sa.engine.url.URL.create(**database_settings)
        self.connect()
    def connect(self):
        pool = sa.create_engine(self.url)
        self.connector = pool.connect(**self.db_settings)
        self.user = User(self)
        self.group = Group(self)
        self.sticker_info = Sticker(self)
    def get_top_by_rating(self, group_id):
        sql_get_top = f"SELECT user_id, rating FROM users_rating WHERE group_id='{group_id}'"
        toplist = []
        for user_rating in self.connector.execute(sql_get_top).fetchall():
            user_id = user_rating[0]
            _, _, fullname = self.user.get_info(user_id)
            toplist.append([fullname, user_rating[1]])
        return sorted(toplist, key=lambda l: l[1], reverse=True)
    def get_rating(self, group_id, user_id):
        sql_rating = f"SELECT rating FROM users_rating WHERE user_id='{user_id}' AND group_id='{group_id}'"
        return self.connector.execute(sql_rating).fetchone()
    def add_rating(self, group_id, user_id, rating=0):
        sql_relations = f"INSERT INTO users_rating(user_id, group_id, rating) VALUES('{user_id}', '{group_id}', {rating})"
        self.connector.execute(sql_relations)
        self.connector.commit()
    def set_rating(self, group_id, user_id, rating):
        current_rating = self.get_rating(group_id, user_id)[0]
        sql_update_rating = f"UPDATE users_rating SET rating={current_rating+rating} WHERE user_id='{user_id}' AND group_id='{group_id}'"
        self.connector.execute(sql_update_rating)
        self.connector.commit()
        return current_rating+rating
    