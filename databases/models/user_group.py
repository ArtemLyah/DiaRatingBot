from sqlalchemy.orm import relationship
from databases.models.users import Users
from databases.models.groups import Groups
from loader import Database
import sqlalchemy as sa

class UserGroup(Database.Base):
    __tablename__ = "userGroup"
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.String, sa.ForeignKey("users.id"))
    group_id = sa.Column(sa.String, sa.ForeignKey("groups.id"))
    local_rating = sa.Column(sa.Integer, default=0)
    is_ban = sa.Column(sa.Boolean, default=False)
    
    users = relationship("Users", back_populates="userGroup")
    groups = relationship("Groups", back_populates="userGroup")

Users.userGroup = relationship("UserGroup", order_by=UserGroup.id, back_populates="users")
Groups.userGroup = relationship("UserGroup", order_by=UserGroup.id, back_populates="groups")