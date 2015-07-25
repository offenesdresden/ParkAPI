import os

from park_api import structs, security
import importlib
import configparser
import sys

API_VERSION = '1.0'
SERVER_VERSION = '0.0.0'
SOURCE_REPOSITORY = 'https://github.com/offenesdresden/ParkAPI'

APP_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))

SERVER_CONF = None
ENV = None
SUPPORTED_CITIES = None
DATABASE = {}

DEFAULT_CONFIGURATION = {
    "port": 5000,
    "host": "::1",
    "debug": False,
    "live_scrape": True,
    "database_host": "127.0.0.1",
    "database_port": 5432,
    "database_name": "park_api",
    "database_user": None,
    "database_password": None,
}


def is_production():
    return ENV == "production"


def is_development():
    return ENV == "development"


def is_testing():
    return ENV == "testing"


def is_staging():
    return ENV == "staging"


def getuser():
    for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
        user = os.environ.get(name)
        if user:
            return user

    # If this fails, the exception will "explain" why
    import pwd
    return pwd.getpwuid(os.getuid())[0]


def database_config(config):
    conf = {
        "host": config.get("database_host"),
        "port": config.get("database_port"),
        "database": config.get("database_name"),
        "password": config.get("database_password"),
    }
    user = config.get("database_user")
    if user == None or len(user) == 0:
        conf["user"] = getuser()
    else:
        conf["user"] = user
    return conf


def load_cities():
    """
    Iterate over files in park_api/cities to add them to list of available cities.
    This list is used to stop requests trying to access files and output them which are not cities.
    """
    cities = {}
    path = os.path.join(APP_ROOT, "park_api", "cities")
    for file in filter(security.file_is_allowed, os.listdir(path)):
        city = importlib.import_module("park_api.cities." + file.title()[:-3])
        cities[file[:-3]] = city
    return cities


def supported_cities():
    global SUPPORTED_CITIES
    if SUPPORTED_CITIES is None:
        SUPPORTED_CITIES = load_cities()
    return SUPPORTED_CITIES


def load_config():
    global ENV
    ENV = os.getenv("env", "development")

    config_path = os.path.join(APP_ROOT, "config.ini")
    try:
        config_file = open(config_path)
    except (OSError, FileNotFoundError) as e:
        print("Failed load configuration: %s" % e)
        exit(1)
    config = configparser.ConfigParser(DEFAULT_CONFIGURATION, strict=False)
    config.read_file(config_file)

    try:
        raw_config = config[ENV]
    except KeyError:
        print("environment '%s' does not exists in config.ini" % ENV, file=sys.stderr)
        exit(1)

    global SERVER_CONF, DATABASE, SUPPORTED_CITIES, LIVE_SCRAPE
    SERVER_CONF = structs.ServerConf(host=raw_config.get('host'),
                                     port=raw_config.getint("port"),
                                     debug=raw_config.getboolean("debug"))
    LIVE_SCRAPE = raw_config.getboolean("live_scrape")
    DATABASE = database_config(raw_config)


load_config()
