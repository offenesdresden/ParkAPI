import pytz
from datetime import datetime
from os import path
import json
import psycopg2
import configparser


def get_most_lots_from_json(city, lot_name):
    """
    Get the total value from the highest known value in the last saved JSON.
    This is useful for cities that don't publish total number of spaces for a parking lot.

    Caveats:
     - Returns 0 if not found.
     - If a lot name exists twice only the last value is returned.

    :param city:
    :param lot_name:
    :return:
    """

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
        cursor.execute("SELECT data FROM parkapi_test WHERE city=%s;", (city,))
        all_data = cursor.fetchall()

        most_lots = 0
        for json_data in all_data:
            lots = json_data[0]["lots"]
            for lot in lots:
                if lot["name"] == lot_name:
                    if int(lot["total"]) > most_lots:
                        most_lots = int(lot["total"])
        return most_lots


def utc_now():
    """
    Returns the current UTC time in ISO format.

    :return:
    """
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
