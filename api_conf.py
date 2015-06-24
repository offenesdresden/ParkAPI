from os.path import join, dirname
import structs

API_VERSION = '1.0'
SERVER_VERSION = '0.0.1'
SOURCE_REPOSITORY = 'https://github.com/offenesdresden/ParkAPI'
CACHE_DIRECTORY = join(dirname(__file__), 'cache')

DEFAULT_SERVER = structs.ServerConf(
    port=5000,
    host='localhost',
)

del join, dirname, structs
