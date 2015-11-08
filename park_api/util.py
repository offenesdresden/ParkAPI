import pytz
from datetime import datetime


def utc_now():
    """
    Returns the current UTC time in ISO format.

    :return:
    """
    return datetime.utcnow().replace(microsecond=0).isoformat()


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
        "\"": "",
        "/": "",
        "\\": "",
        "\n": "",
        "\t": ""
    }
    for repl in replacements.keys():
        string = string.replace(repl, replacements[repl])
    return string


def parse_date(date_string, date_format, timezone="Europe/Berlin"):
    """
    Convert a date into a ISO formatted UTC date string.
    Timezone defaults to Europe/Berlin.

    :param date_string:
    :param date_format:
    :param timezone:
    :return:
    """
    last_updated = datetime.strptime(date_string, date_format)
    local_timezone = pytz.timezone(timezone)
    last_updated = local_timezone.localize(last_updated, is_dst=None)
    last_updated = last_updated.astimezone(pytz.utc).replace(tzinfo=None)

    return last_updated.replace(microsecond=0)
