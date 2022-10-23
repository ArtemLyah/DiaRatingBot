from .user_middleware import GetDBUserMiddleware
from dispatcher import dp

dp.middleware.setup(GetDBUserMiddleware())
