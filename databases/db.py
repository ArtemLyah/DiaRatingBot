import sqlalchemy as sa
from config import database_settings
from .user_settings import Rating, IsBan

class Database():
    def __init__(self, database_settings) -> None:
        """
        Database of DiaBot
        Connects to postgre database by sqlalchemy

        :param database_settings: settings like host, user, password, database, port
        :type database_settings: :obj:`dict`

        """
        self.db_settings = database_settings

    def connect(self):
        """
        Creates pool by :obj:`sa.create_engine(self.url)` and makes connection to database
        
        :new atribute connector: creates by pool 
        :atribute type: :obj:`sa.engine.Connection`

        """
        url = sa.engine.url.URL.create(**self.db_settings)
        pool = sa.create_engine(url)
        self.connector = pool.connect()
        

class Users():
    def __init__(self, db:Database) -> None:
        """
        Table 'users'
        Contain information about user: id, username, fullname

        :param db: database object 
        :type db: :obj:`Database`

        """
        self.db = db

    def get_info(self, user_id):
        """
        Get information about user from table 'users'

        :param user_id: user's id from :obj:`message.from_user.id`

        :return: user_id, username, fullname
        :rtype: str, str, str

        """
        sql = f"SELECT id, username, fullname FROM users WHERE id='{user_id}'"
        return self.db.connector.execute(sql).fetchone()

    def add(self, user_id, username, fullname):
        """
        Add new user to table 'users'

        :param user_id: user's id from :obj:`message.from_user.id`
        :param username: user's username or tag from :obj:`message.from_user.username`
        :param fullname: user's fullname from :obj:`message.from_user.fullname`

        """
        if not self.get_info(user_id):
            sql_user_info = f"INSERT INTO users(id, username, fullname) VALUES('{user_id}', '{username}', '{fullname}')"
            self.db.connector.execute(sql_user_info)

class Groups():
    def __init__(self, db:Database) -> None:
        """
        Table 'groups'
        Contain information about group: id, username, fullname

        :param db: database object 
        :type db: :obj:`Database`

        """
        self.db = db

    def get_info(self, id):
        """
        Get information about group from table 'groups'

        :param id: group's id from :obj:`message.chat.id`

        :return: group_id, username, fullname
        :rtype: str, str, str

        """
        sql = f"SELECT * FROM groups WHERE id='{id}'"
        return self.db.connector.execute(sql).fetchone()

    def add(self, group_id, username, name):
        """
        Add new group to table 'groups'

        :param group_id: group's id from :obj:`message.chat.id`
        :param username: group's username or tag from :obj:`message.chat.username`
        :param name: group's fullname from :obj:`message.chat.fullname` 

        """
        if not self.get_info(group_id):
            sql_group_info = f"INSERT INTO groups(id, username, name) VALUES('{group_id}', '{username}', '{name}')"
            self.db.connector.execute(sql_group_info)

class Stickers():
    def __init__(self, db:Database) -> None:
        """
        Set of stickers with dia marks in table 'stickers'
        Contain information about sticker: unique_file_id, rating

        :param db: database object 
        :type db: :obj:`Database`

        """
        self.db = db

    def get_info(self, unique_file_id):
        """
        Get information about sticker from table 'stickers'

        :param unique_file_id: unique id of sticker from :obj:`message.sticker.thumb.file_unique_id`
        :type unique_file_id: str

        :return: rate of sticker
        :rtype: int

        """
        sql = f"SELECT rate FROM stickers WHERE unique_file_id='{unique_file_id}'"
        sticker = self.db.connector.execute(sql).fetchone()
        return sticker[0] if sticker else None

    def add_sticker(self, unique_file_id, rate):
        """
        Add new sticker to 'stickers'

        :param unique_file_id: unique id of sticker from :obj:`message.sticker.thumb.file_unique_id`
        :param rate: rate of sticker

        """
        if not self.get_info(unique_file_id):
            sql_stickers = f"INSERT INTO stickers(unique_file_id, rate) VALUES('{unique_file_id}', {rate})"
            self.db.connector.execute(sql_stickers)

class UsersStatus():
    def __init__(self, db:Database) -> None:
        """
        Object of table 'user_status'
        'user_status' contain: user_id, group_id, rating, is_ban
        
        :param db: database object
        :type db: :obj:`Database`
        """
        self.db = db
        self.rating = Rating(self.db)
        self.isban = IsBan(self.db)

    def get_top_by_rating(self, group_id):
        """
        Create toplist of users in group

        :param group_id: group's id from :obj:`message.chat.id`

        :return: list_of_users [[full_name_1, rating_1], [full_name_2, rating_2], ...] sorted by max rating

        """
        sql_get_top = f"SELECT user_id, rating FROM users_status WHERE group_id='{group_id}'"
        toplist = []
        for user_rating in self.db.connector.execute(sql_get_top).fetchall():
            user_id = user_rating[0]
            _, _, fullname = users.get_info(user_id)
            toplist.append([fullname, user_rating[1]])
        return sorted(toplist, key=lambda l: l[1], reverse=True)

    def get_status(self, group_id, user_id):
        sql_status = f"SELECT * FROM users_status WHERE group_id='{group_id}' AND user_id='{user_id}'"
        status = self.db.connector.execute(sql_status).fetchone()
        return status[0] if status else None

    def add_status(self, group_id, user_id, rating=0, isban=False):
        sql_relations = "INSERT INTO users_status(user_id, group_id, rating, is_ban) "+\
                        f"VALUES('{user_id}', '{group_id}', {rating}, {isban})"
        self.db.connector.execute(sql_relations)

    def remove_status(self, user_id, group_id):
        sql_delete = f"DELETE FROM users_status WHERE user_id = '{user_id}' AND group_id='{group_id}'"
        self.db.connector.execute(sql_delete)

if __name__ != "__main__":
    database = Database(database_settings)
    database.connect()
    users = Users(database)
    groups = Groups(database)
    stickers = Stickers(database)
    users_status = UsersStatus(database)