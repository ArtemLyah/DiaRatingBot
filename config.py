from dotenv import load_dotenv
import os


# load data from .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

father_id = 905143300

database_settings = {
    "host" : os.getenv("db_h"),
    "user" : os.getenv("db_u"),
    "password" : os.getenv("db_pwd"),
    "database" : os.getenv("db_db")
}

