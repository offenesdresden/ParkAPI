import pytz
from datetime import datetime


def utc_now():
    return datetime.utcnow().replace(microsecond=0).isoformat()


def convert_date(date_string, date_format, timezone="Europe/Berlin"):
    """
    Take a date_string and format and return an UTC representation in ISO format.
    Date is always expected in Europe/Berlin timezone unless specified otherwise.
    """
    last_updated = datetime.strptime(date_string, date_format)
    local_timezone = pytz.timezone(timezone)
    last_updated = local_timezone.localize(last_updated, is_dst=None)
    last_updated = last_updated.astimezone(pytz.utc).replace(tzinfo=None)

    return last_updated.replace(microsecond=0).isoformat()

def remove_special_chars(string):
    replacements = {
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "ß": "ss",
        "-": "",
        " ": "",
        ".": "",
        ",": ""
    }
    for repl in replacements.keys():
        string = string.replace(repl, replacements[repl])
    return string

