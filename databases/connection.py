from . import * 
from utils.logs import logger
import config

def connectDatabase():
    db = Database(config.db_settings)
    db.connect()
    logger.debug("Connected to database")

    if config.create_db:
        db.create_tables()
        logger.debug("Create tables in database")
    return db