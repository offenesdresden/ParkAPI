from os.path import join, dirname
import types


VERSION = '1.0'
SOURCE_REPOSITORY = 'https://github.com/offenesdresden/ParkAPI'
CACHE_DIRECTORY = join(dirname(__file__), 'cache')

DEFAULT_SERVER = types.ServerConf(
    port = 5000,
    host = 'localhost',
    mail = ''
)

del join, dirname, tools
