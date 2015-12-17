import os
from yoyo import read_migrations, get_backend

from park_api import env


def main():
    backend = get_backend(env.DATABASE_URI)
    migrations = read_migrations(os.path.join(env.APP_ROOT, "schema/db"))
    backend.apply_migrations(migrations)

if __name__ == "__main__":
    main()
