from sqlalchemy.orm import relationship
from databases.models.users import Users
from loader import Database
from utils.mics import next_update_day

import sqlalchemy as sa

class Rusak(Database.Base):
    __tablename__ = "rusak"
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.String, sa.ForeignKey("users.id"))
    name = sa.Column(sa.String)
    intellect = sa.Column(sa.Integer)
    strength = sa.Column(sa.Integer)
    rashism = sa.Column(sa.Integer)
    health = sa.Column(sa.Integer)
    photo_id = sa.Column(sa.Integer)
    
    users = relationship("Users", back_populates="rusak")

Users.rusak = relationship("Rusak", order_by=Users.id, back_populates="users")