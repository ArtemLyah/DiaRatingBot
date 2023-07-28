from sqlalchemy.orm import relationship
from .database import Database
from utils.mics import next_update_day
import sqlalchemy as sa

class Users(Database.Base):
    __tablename__ = "users"
    id = sa.Column(sa.BigInteger, unique=True, primary_key=True)
    full_name = sa.Column(sa.String)
    username = sa.Column(sa.String)
    
class Groups(Database.Base):
    __tablename__ = "groups"
    id = sa.Column(sa.BigInteger, unique=True, primary_key=True)
    fullname = sa.Column(sa.String)

class UserGroup(Database.Base):
    __tablename__ = "userGroup"
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.BigInteger, sa.ForeignKey("users.id"))
    group_id = sa.Column(sa.BigInteger, sa.ForeignKey("groups.id"))
    local_rating = sa.Column(sa.Integer, default=0)
    is_ban = sa.Column(sa.Boolean, default=False)
    
    users = relationship("Users", back_populates="userGroup")
    Users.userGroup = relationship("UserGroup", order_by=id, back_populates="users")
    
    groups = relationship("Groups", back_populates="userGroup")
    Groups.userGroup = relationship("UserGroup", order_by=id, back_populates="groups")

class UserRandom(Database.Base):
    __tablename__ = "userRandom"
    id = sa.Column(sa.Integer, primary_key=True)
    user_group_id = sa.Column(sa.Integer, sa.ForeignKey("userGroup.id"))
    text_id = sa.Column(sa.Integer)
    date_update = sa.Column(sa.Date, default=next_update_day())

    userGroup = relationship("UserGroup", back_populates="userRandom")
    UserGroup.userRandom = relationship("UserRandom", order_by=id, back_populates="userGroup")

class Countings(Database.Base):
    __tablename__ = "countings"
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.BigInteger, sa.ForeignKey("users.id"))
    count_mining = sa.Column(sa.Integer, default=0)
    count_rating = sa.Column(sa.Integer, default=0)
    count_present = sa.Column(sa.Integer, default=0)
    update_limit_date = sa.Column(sa.Date, default=next_update_day())
    
    users = relationship("Users", back_populates="countings")
    Users.countings = relationship("Countings", order_by=Users.id, back_populates="users")

class Rusak(Database.Base):
    __tablename__ = "rusak"
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.BigInteger, sa.ForeignKey("users.id"))
    name = sa.Column(sa.String)
    intellect = sa.Column(sa.Integer)
    strength = sa.Column(sa.Integer)
    rashism = sa.Column(sa.Integer)
    health = sa.Column(sa.Integer)
    photo_id = sa.Column(sa.Integer)
    
    users = relationship("Users", back_populates="rusak")
    Users.rusak = relationship("Rusak", order_by=Users.id, back_populates="users")

class Stickers(Database.Base):
    __tablename__ = "stickers"
    id = sa.Column(sa.Integer, primary_key=True)
    file_id = sa.Column(sa.String)
    rating = sa.Column(sa.Integer)


