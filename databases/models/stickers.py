from loader import Database
import sqlalchemy as sa

class Stickers(Database.Base):
    __tablename__ = "stickers"
    id = sa.Column(sa.Integer, primary_key=True)
    file_id = sa.Column(sa.String)
    rating = sa.Column(sa.Integer)