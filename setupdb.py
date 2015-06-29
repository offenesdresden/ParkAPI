import psycopg2
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

db_data = {
    "host": config["Database"]["host"],
    "name": config["Database"]["name"],
    "user": config["Database"]["user"],
    "pass": config["Database"]["pass"],
    "port": config["Database"]["port"]
}

with psycopg2.connect(database=db_data["name"], user=db_data["user"], host=db_data["host"], port=db_data["port"],
                      password=db_data["pass"]) as conn:

    cursor = conn.cursor()
    cursor.execute('CREATE TABLE "public"."parkapi" ('
                   '"id" SERIAL,'
                   '"timestamp_updated" TIMESTAMP NOT NULL,'
                   '"timestamp_downloaded" TIMESTAMP NOT NULL,'
                   '"city" TEXT NOT NULL,"data" JSON NOT NULL,'
                   'PRIMARY KEY ("id"))'
                   'TABLESPACE "pg_default";')
    conn.commit()
