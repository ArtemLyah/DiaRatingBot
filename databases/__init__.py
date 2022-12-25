from config import database_settings
from .db import Database, Users, Groups, Stickers, UsersStatus


database = Database(database_settings)
database.connect()
users = Users(database)
groups = Groups(database)
stickers = Stickers(database)
users_status = UsersStatus(database)