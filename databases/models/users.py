from loader import Database
import sqlalchemy as sa

class Users(Database.Base):
    __tablename__ = "users"
    id = sa.Column(sa.Text, unique=True, primary_key=True)
    full_name = sa.Column(sa.String)
    username = sa.Column(sa.String)
    