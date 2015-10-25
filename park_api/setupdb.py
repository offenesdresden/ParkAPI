import os
from yoyo import read_migrations
from yoyo.connections import connect

from park_api import env


def main():
    conn, paramstyle = connect(env.DATABASE_URI)
    schema_path = os.path.join(env.APP_ROOT, "schema/db")
    migrations = read_migrations(conn, paramstyle, schema_path)
    migrations.to_apply().apply()
    conn.commit()

if __name__ == "__main__":
    main()
