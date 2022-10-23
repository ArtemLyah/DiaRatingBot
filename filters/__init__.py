from .group_filter import IsGroup, IsReplyDiaStickers
from dispatcher import dp

if __name__ == "filters":
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsReplyDiaStickers)