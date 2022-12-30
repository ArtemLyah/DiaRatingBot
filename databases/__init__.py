from config import database_settings
from .db import Database, Users, Groups, Stickers, UserStatus


database = Database(database_settings)
database.connect()
users = Users(database)
groups = Groups(database)
stickers = Stickers(database)
user_status = UserStatus(database)