import sqlalchemy
pool = sqlalchemy.create_engine(
    # Equivalent URL:
    # postgresql+pg8000://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
    sqlalchemy.engine.url.URL.create(
        drivername="postgresql+psycopg2",
        username="postgres",
        password=")~l,ABj_X@t+ZaY)",
        host="34.79.229.60",
        port=5432,
        database="diarating",
    )
)

connector = pool.connect()
print(connector.execute("SELECT * FROM groups").fetchall())
