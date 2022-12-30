from config import database_settings
import sqlalchemy
pool = sqlalchemy.create_engine(
    # Equivalent URL:
    # postgresql+pg8000://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
    sqlalchemy.engine.url.URL.create(**database_settings)
)

connector = pool.connect()
print(connector.execute("SELECT * FROM groups").fetchall())
