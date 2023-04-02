from sqlalchemy.orm import relationship
from databases.models import UserGroup
from loader import Database
from utils.mics import next_update_day
import sqlalchemy as sa

class UserRandom(Database.Base):
    __tablename__ = "userRandom"
    id = sa.Column(sa.Integer, primary_key=True)
    user_group_id = sa.Column(sa.Integer, sa.ForeignKey("userGroup.id"))
    text_id = sa.Column(sa.Integer)
    date_update = sa.Column(sa.Date, default=next_update_day())

    userGroup = relationship("UserGroup", back_populates="userRandom")

UserGroup.userRandom = relationship("UserRandom", order_by=UserRandom.id, back_populates="userGroup")