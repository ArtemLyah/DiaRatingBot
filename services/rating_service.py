from databases import Users, UserGroup
from loader import db_session
from sqlalchemy.sql import func
from sqlalchemy.sql import and_, desc

class RatingService():
    def addRating(self, user_group, rating=0) -> int:
        updateUserGroup = {
            UserGroup.local_rating : user_group.local_rating+rating
        }
        db_session.query(UserGroup)\
            .filter(
                and_(
                    UserGroup.group_id == user_group.group_id, 
                    UserGroup.user_id == user_group.user_id
                )
            ).update(updateUserGroup, synchronize_session=False)
        db_session.commit()
        return user_group.local_rating

    def calculateLimit(self, user_id=None) -> int:
        rating = self.calculateGlobalRating(user_id)
        if rating < -500:
            return 0
        elif rating < -200:
            return 10 
        elif rating < 100:
            return 20
        return (rating // 10)*2
    
    def calculateGlobalRating(self, user_id) -> int:
        return db_session.query(
            func.sum(UserGroup.local_rating))\
                .filter(UserGroup.user_id == str(user_id))\
                    .first()[0]

    def get_top_10(self) -> list[tuple[str, int]]:
        return db_session.query(Users.full_name, func.sum(UserGroup.local_rating))\
            .join(UserGroup)\
                .group_by(Users)\
                    .order_by(desc(func.sum(UserGroup.local_rating)))\
                        .limit(10)\
                            .all()

    def get_top_group(self, group_id) -> list[tuple[str, int]]:
        return db_session.query(Users.full_name, UserGroup.local_rating)\
            .join(UserGroup)\
                .filter(UserGroup.group_id == str(group_id))\
                    .order_by(desc(UserGroup.local_rating))\
                        .all()
