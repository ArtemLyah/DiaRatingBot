import psycopg2 as pg
from config import database_settings

class User():
    def __init__(self, db) -> None:
        self.db = db
    def get_info(self, id):
        sql = f"SELECT id, username, fullname FROM users_info WHERE id='{id}'"
        self.db.cursor.execute(sql)
        return self.db.cursor.fetchone()
    def add(self, group_id, id, username, fullname):
        sql_user_info = f"INSERT INTO users_info(id, username, fullname) VALUES('{id}', '{username}', '{fullname}')"
        self.db.cursor.execute(sql_user_info)
        sql_relations = f"INSERT INTO users_rating(user_id, group_id) VALUES('{id}', '{group_id}')"
        self.db.cursor.execute(sql_relations)
        self.db.connection.commit()
    
class Group():
    def __init__(self, db) -> None:
        self.db = db
    def get_info(self, id):
        sql = f"SELECT * FROM groups_info WHERE id='{id}'"
        self.db.cursor.execute(sql)
        return self.db.cursor.fetchone()
    def add(self, id, username, name):
        if not self.get_info(id):
            sql_group_info = f"INSERT INTO groups_info(id, username, name) VALUES('{id}', '{username}', '{name}')"
            self.db.cursor.execute(sql_group_info)
            self.db.connection.commit()

class Status():
    def __init__(self, db) -> None:
        self.db = db
    def get_rate(self, unique_file_id):
        sql = f"SELECT rate FROM status_info WHERE unique_file_id={unique_file_id}"
        self.db.cursor.execute(sql)
        return self.db.cursor.fetchone()
    def add_rate(self, unique_file_id, rate):
        sql_status_info = f"INSERT INTO status_info(unique_file_id, rate) VALUES('{unique_file_id}', {rate})"
        self.db.cursor.execute(sql_status_info)
        self.db.connection.commit()
        
class Database():
    def __init__(self, user, password, database, host="localhost") -> None:
        self.db_settings = database_settings
        self.connection = pg.connect(**database_settings)
        self.cursor = self.connection.cursor()
        self.user = User(self)
        self.group = Group(self)
        self.status_info = Status(self)
    def reload(self):
        self.connection = pg.connect(self.db_settings)
        self.cursor = self.connection.cursor()
        self.user = User(self)
        self.group = Group(self)
    def get_top_by_rating(self, group_id):
        sql_get_top = f"SELECT user_id, rating FROM users_rating WHERE group_id='{group_id}'"
        self.cursor.execute(sql_get_top)
        toplist = []
        for user_rating in self.cursor.fetchall():
            user_id = user_rating[0]
            _, _, fullname = self.user.get_info(user_id)
            toplist.append([fullname, user_rating[1]])
        return sorted(toplist, key=lambda l: l[1], reverse=True)
    def get_rating(self, group_id, user_id):
        sql_rating = f"SELECT rating FROM users_rating WHERE user_id='{user_id}' AND group_id='{group_id}'"
        self.cursor.execute(sql_rating)
        return self.cursor.fetchone()
    def add_rating(self, group_id, user_id, rating=0):
        sql_relations = f"INSERT INTO users_rating(user_id, group_id, rating) VALUES('{user_id}', '{group_id}', {rating})"
        self.cursor.execute(sql_relations)
        self.connection.commit()
    def set_rating(self, group_id, user_id, rating):
        current_rating = self.get_rating(group_id, user_id)[0]
        sql_update_rating = f"UPDATE users_rating SET rating={current_rating+rating} WHERE user_id='{user_id}' AND group_id='{group_id}'"
        self.cursor.execute(sql_update_rating)
        self.connection.commit()
        return current_rating+rating
    