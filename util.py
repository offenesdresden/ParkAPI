import pytz
from datetime import datetime
from os import path


# if city does not send totals, we can push totals to the higest known value
# saved in the json file
# if the lot_name does not exits returns 0
# problem: if one lot name exist twice, it takes always the last value
# but the same lot name should never exists more than one time 
def get_lots_from_json ( city, lot_name ) :
    lots = 0
    last_values_json = "cache/"+city+".json" 
    if os.path.isfile(last_values_json):
        with open(last_values_json) as data_file:
            last_values = json.load(data_file)
            if last_values is None :
                # if no last json file exists, return 0
                return 0
            for lastlots in last_values["lots"] :
                if lastlots["name"] is lot_name:
                    lots = int(lastlots["total"])
    return lots



def utc_now():
    return datetime.utcnow().replace(microsecond=0).isoformat()


def convert_date(date_string, date_format, timezone="Europe/Berlin"):
    """
    Convert a date into a ISO formatted UTC date string. Timezone defaults to Europe/Berlin.

    :param date_string:
    :param date_format:
    :param timezone:
    :return:
    """
    last_updated = datetime.strptime(date_string, date_format)
    local_timezone = pytz.timezone(timezone)
    last_updated = local_timezone.localize(last_updated, is_dst=None)
    last_updated = last_updated.astimezone(pytz.utc).replace(tzinfo=None)

    return last_updated.replace(microsecond=0).isoformat()


def remove_special_chars(string):
    """
    Remove any umlauts, spaces and punctuation from a string.
    :param string:
    :return:
    """
    replacements = {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "ß": "ss",
        "-": "",
        " ": "",
        ".": "",
        ",": "",
        "'": "",
        "\"": ""
    }
    for repl in replacements.keys():
        string = string.replace(repl, replacements[repl])
    return string


def generate_id(city_file_path, lot_name):
    """
    Generate an ID for a parking lot by concatenating city name and lot name.

    :param city_file_path: __file__ for the city file
    :param lot_name: Name of the parking lot
    :return: ID
    """
    return remove_special_chars((path.basename(city_file_path)[:-3] + lot_name).lower())
