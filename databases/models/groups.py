from loader import Database
import sqlalchemy as sa

class Groups(Database.Base):
    __tablename__ = "groups"
    id = sa.Column(sa.Text, unique=True, primary_key=True)
    fullname = sa.Column(sa.String)