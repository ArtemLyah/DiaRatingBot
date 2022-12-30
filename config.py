from dotenv import load_dotenv
import os


# load data from .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

FATHER_ID = int(os.getenv("father_id"))

database_settings = {
    "drivername":"postgresql+psycopg2",
    "username":os.getenv("db_u"),
    "password":os.getenv("db_pwd"),
    "host":os.getenv("db_h"),
    "port":5432,
    "database":os.getenv("db_db")
}

