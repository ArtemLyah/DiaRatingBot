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
            max_overflow=2,
            pool_recycle=300,
            pool_use_lifo=True
        )
        self.connector = self.engine.connect()
        self.session = sessionmaker(self.engine)()