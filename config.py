from dotenv import load_dotenv
import os

# load data from .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS = [905143300, 572127054, 907720594]

db_settings = {
    "drivername":"postgresql+psycopg2",
    "username":os.getenv("DB_USER"),
    "password":os.getenv("DB_PASSWORD"),
    "host":os.getenv("DB_HOST"),
    "port":os.getenv("DB_PORT"),
    "database":os.getenv("DB_NAME")
}
    
create_db = True