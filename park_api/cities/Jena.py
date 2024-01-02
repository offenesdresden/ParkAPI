import json
import requests
import pytz
from datetime import datetime, time
from bs4 import BeautifulSoup
from park_api import env
from park_api.geodata import GeoData
from park_api.util import convert_date

# there is no need for any geodata for this file, as the api returns all of the information,
# but if this is removed, the code crashes
geodata = GeoData(__file__)

def parse_html(lot_vacancy_xml):

    # there is a second source with all the general data for the parking lots
    HEADERS = {
        "User-Agent": "ParkAPI v%s - Info: %s" %
        (env.SERVER_VERSION, env.SOURCE_REPOSITORY),
    }

    lot_data_json   = requests.get("https://opendata.jena.de/dataset/1a542cd2-c424-4fb6-b30b-d7be84b701c8/resource/76b93cff-4f6c-47fa-ab83-b07d64c8f38a/download/parking.json", headers={**HEADERS})

    lot_vacancy = BeautifulSoup(lot_vacancy_xml, "xml")
    lot_data = json.loads(lot_data_json.text)

    data = {
        # the time contains the timezone and milliseconds which need to be stripped
        "last_updated": lot_vacancy.find("publicationTime").text.split(".")[0],
        "lots": []
    }

    for lot in lot_data["parkingPlaces"]:
        # the lots from both sources need to be matched
        lot_data_list = [
            _lot for _lot in lot_vacancy.find_all("parkingFacilityStatus")
                if hasattr(_lot.parkingFacilityReference, "attr")
                and _lot.parkingFacilityReference.attrs["id"] == lot["general"]["name"]
        ]

        lot_id = lot["general"]["name"].lower().replace(" ", "-").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")

        lot_info = {
            "id": lot_id,
            "name": lot["general"]["name"],
            "url": "https://mobilitaet.jena.de/de/" + lot_id,
            "address": lot["details"]["parkingPlaceAddress"]["parkingPlaceAddress"],
            "coords": lot["general"]["coordinates"],
            "state": get_status(lot),
            "lot_type": lot["general"]["objectType"],
            "opening_hours": parse_opening_hours(lot),
            "fee_hours": parse_charged_hours(lot),
            "forecast": False,
        }

        # some lots do not have live vacancy data
        if len(lot_data_list) > 0:
            lot_info["free"] = int(lot_data_list[0].totalNumberOfVacantParkingSpaces.text)
            lot_info["total"] = int(lot_data_list[0].totalParkingCapacityShortTermOverride.text)
        else:
            continue
            # lot_info["free"] = None
            # lot_info["total"] = int(lot["details"]["parkingCapacity"]["totalParkingCapacityShortTermOverride"])
        # note: both api's have different values for the total parking capacity,
        # but the vacant slot are based on the total parking capacity from the same api,
        # so that is used if available

        # also in the vacancy api the total capacity for the "Goethe Gallerie" are 0 if it is closed


        data["lots"].append(lot_info)

    return data

# the rest of the code is there to deal with the api's opening/charging hours objects
# example:
# "openingTimes": [
#   {
#     "alwaysCharged": True,
#     "dateFrom": 2,
#     "dateTo": 5,
#     "times": [
#       {
#         "from": "07:00",
#         "to": "23:00"
#       }
#     ]
#   },
#   {
#     "alwaysCharged": False,
#     "dateFrom": 7,
#     "dateTo": 1,
#     "times": [
#       {
#         "from": "10:00",
#         "to": "03:00"
#       }
#     ]
#   }
# ]

def parse_opening_hours(lot_data):
    if lot_data["parkingTime"]["openTwentyFourSeven"]: return "24/7"

    return parse_times(lot_data["parkingTime"]["openingTimes"])

def parse_charged_hours(lot_data):
    charged_hour_objs = []

    ph_info = "An Feiertagen sowie außerhalb der oben genannten Zeiten ist das Parken gebührenfrei."

    if not lot_data["parkingTime"]["chargedOpeningTimes"] and lot_data["parkingTime"]["openTwentyFourSeven"]:
        if lot_data["priceList"]:
            if ph_info in str(lot_data["priceList"]["priceInfo"]):
                return "24/7; PH off"
            else: return "24/7"
        else: return "off"

    # charging hours can also be indicated by the "alwaysCharged" variable in "openingTimes"
    elif not lot_data["parkingTime"]["chargedOpeningTimes"] and not lot_data["parkingTime"]["openTwentyFourSeven"]:
        for oh in lot_data["parkingTime"]["openingTimes"]:
            if "alwaysCharged" in oh and oh["alwaysCharged"]: charged_hour_objs.append(oh)
        if len(charged_hour_objs) == 0: return "off"

    elif lot_data["parkingTime"]["chargedOpeningTimes"]:
        charged_hour_objs = lot_data["parkingTime"]["chargedOpeningTimes"]

    charged_hours = parse_times(charged_hour_objs)

    if ph_info in str(lot_data["priceList"]["priceInfo"]):
        charged_hours += "; PH off"

    return charged_hours

# creatin osm opening_hours strings from opening/charging hours objects
def parse_times(times_objs):
    DAYS = ["", "Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

    ohs = ""

    for index, oh in enumerate(times_objs):
        part = ""

        if oh["dateFrom"] == oh["dateTo"]:
            part += DAYS[oh["dateFrom"]]
        else:
            part += DAYS[oh["dateFrom"]] + "-" + DAYS[oh["dateTo"]]

        part += " "

        for index2, time in enumerate(oh["times"]):
            part += time["from"] +  "-" + time["to"]
            if index2 != len(oh["times"]) - 1: part += ","

        if index != len(times_objs) - 1: part += "; "

        ohs += part

    return ohs

def get_status(lot_data):
    if lot_data["parkingTime"]["openTwentyFourSeven"]: return "open"

    # check for public holiday?

    for oh in lot_data["parkingTime"]["openingTimes"]:
        now = datetime.now(pytz.timezone("Europe/Berlin"))

        weekday = now.weekday() + 1

        # oh rules can also go beyond week ends (e.g. from Sunday to Monday)
        # this need to be treated differently
        if oh["dateFrom"] <= oh["dateTo"]:
            if not (weekday >= oh["dateFrom"]) or not (weekday <= oh["dateTo"] + 1): continue
        else:
            if weekday > oh["dateTo"] + 1 and weekday < oh["dateFrom"]: continue

        for times in oh["times"]:
            time_from = get_timestamp_without_date(time.fromisoformat(times["from"]).replace(tzinfo=pytz.timezone("Europe/Berlin")))
            time_to = get_timestamp_without_date(time.fromisoformat(times["to"]).replace(tzinfo=pytz.timezone("Europe/Berlin")))

            time_now = get_timestamp_without_date(now)

            # time ranges can go over to the next day (e.g 10:00-03:00)
            if time_to >= time_from:
                if time_now >= time_from and time_now <= time_to:
                    return "open"
                else: continue

            else:
                if oh["dateFrom"] <= oh["dateTo"]:
                    if (time_now >= time_from and weekday >= oh["dateFrom"] and weekday <= oh["dateTo"]
                    or time_now <= time_to and weekday >= oh["dateFrom"] + 1 and weekday <= oh["dateTo"] + 1):
                        return "open"
                    else: continue

                else:
                    if (time_now >= time_from and (weekday >= oh["dateFrom"] or weekday <= oh["dateTo"])
                    or time_now <= time_to and (weekday >= oh["dateFrom"] + 1 or weekday <= oh["dateTo"] + 1)):
                        return "open"
                    else: continue 

    # if no matching rule was found, the lot is closed
    return "closed"

def get_timestamp_without_date (date_obj):
    return date_obj.hour * 3600 + date_obj.minute * 60 + date_obj.second
