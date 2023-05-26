from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa

class Database():
    Base = declarative_base()

    def __init__(self, settings: dict) -> None:
        self.url = sa.engine.url.URL.create(**settings)

    def connect(self):
        self.engine = sa.create_engine(
            self.url, 
            pool_pre_ping=True, 
            connect_args={
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
            },
            pool_use_lifo=True
        )
        self.connector = self.engine.connect()
        self.session = sessionmaker(self.engine)()