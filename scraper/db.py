from urllib.parse import urlparse
from contextlib import contextmanager
import psycopg2, psycopg2.extras
from psycopg2.pool import ThreadedConnectionPool
from park_api import env

POOL = None

def setup(url=env.DATABASE_URI):
    global POOL
    u = urlparse(url)
    POOL = ThreadedConnectionPool(1, 20,
            database=u.path[1:],
            user=u.username,
            password=u.password,
            host=u.hostname,
            port=u.port)

@contextmanager
def cursor(commit=False):
    """
    psycopg2 connection.cursor context manager.
    Creates a new cursor and closes it, commiting changes if specifie
    """
    global POOL
    assert POOL != None, "use db.setup() before calling db.cursor()"
    try:
        connection = POOL.getconn()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            yield cursor
            if commit: connection.commit()
        finally:
            cursor.close()
    finally:
        POOL.putconn(connection)
