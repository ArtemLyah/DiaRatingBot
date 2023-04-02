from sqlalchemy.orm import relationship
from databases.models.users import Users
from loader import Database
from utils.mics import next_update_day

import sqlalchemy as sa

class Countings(Database.Base):
    __tablename__ = "countings"
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.String, sa.ForeignKey("users.id"))
    count_mining = sa.Column(sa.Integer, default=0)
    count_rating = sa.Column(sa.Integer, default=0)
    count_present = sa.Column(sa.Integer, default=0)
    update_limit_date = sa.Column(sa.Date, default=next_update_day().isoformat())
    
    users = relationship("Users", back_populates="countings")

Users.countings = relationship("Countings", order_by=Users.id, back_populates="users")