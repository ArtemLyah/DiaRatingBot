from .user_middleware import GetDBUserMiddleware
from dispatcher import dp

if __name__ != "__main__":
    dp.middleware.setup(GetDBUserMiddleware())
