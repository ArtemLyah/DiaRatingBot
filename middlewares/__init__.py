from .user_middleware import GetDBUserMiddleware
from dispatcher import dp

if __name__ == "user_middleware":
    dp.middleware.setup(GetDBUserMiddleware())
