import psycopg2 as pg
from config import database_settings
connection = pg.connect(**database_settings)
cursor = connection.cursor()
cursor.execute("SELECT * FROM groups")
print(cursor.fetchall())