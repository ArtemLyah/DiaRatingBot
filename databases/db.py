import psycopg2 as pg


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
        sql_group_info = f"INSERT INTO groups_info(id, username, name) VALUES('{id}', '{username}', '{name}')"
        self.db.cursor.execute(sql_group_info)
        self.db.connection.commit()

class Database():
    def __init__(self, user, password, database, host="localhost") -> None:
        self.connection = pg.connect(
            host = host,
            user=user, 
            password=password,
            database=database)
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
        return sorted(toplist, key=lambda l: l[1])
    def get_rating(self, user_id, group_id):
        sql_rating = f"SELECT rating FROM users_rating WHERE user_id='{user_id}' AND group_id='{group_id}'"
        self.cursor.execute(sql_rating)
        return self.cursor.fetchone()
    def add_rating(self, user_id, group_id, rating):
        current_rating = self.get_rating(user_id, group_id)[0]
        sql_update_rating = f"UPDATE users_rating SET rating={current_rating+rating} WHERE user_id='{user_id}' AND group_id='{group_id}'"
        self.cursor.execute(sql_update_rating)
        self.connection.commit()
        return current_rating+rating
    