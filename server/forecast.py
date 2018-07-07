import os
import csv

from park_api import env


def find_forecast(lot_id, time_from, time_to):
    try:
        csv_path = os.path.join(env.APP_ROOT, "forecast_data", lot_id + ".csv")

        with open(csv_path) as csvfile:
            data = {
                "version": 1.0,
                "data": {}
            }
            for row in csv.reader(csvfile):
                if time_from <= row[0] <= time_to:
                    data["data"][row[0]] = row[1]
            return data
    except FileNotFoundError:
        return None
