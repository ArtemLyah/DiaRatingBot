from .group_filter import IsGroup, IsReplyDiaStickers
from .user_filter import IsFatherPrivate
from dispatcher import dp

if __name__ == "filters":
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsReplyDiaStickers)
    dp.filters_factory.bind(IsFatherPrivate)