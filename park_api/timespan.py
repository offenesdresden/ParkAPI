import os
import csv
from datetime import datetime

from park_api import db, env


def timespan(city, lot_id, total, date_from, date_to, version):
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    if date_from > now or version == 1.0:
        data = forecast(lot_id, total, date_from, date_to, version)
    elif date_to < now:
        data = known_timespan_data(city, lot_id, date_from, date_to, version)
    else:
        data = known_timespan_data(city, lot_id, date_from, now, version)
        data.extend(forecast(lot_id, total, now, date_to, version))
    return data


def known_timespan_data(city, lot_id, date_from, date_to, version):
    if version == 1:
        return {}
    elif version == "1.1":
        with db.cursor() as cur:
            sql = '''SELECT timestamp_downloaded, data \
            FROM parkapi \
            WHERE timestamp_downloaded > %s AND timestamp_downloaded < %s AND city = %s'''
            cur.execute(sql, (date_from, date_to, city,))
            data = []
            for row in cur.fetchall():
                for lot in row['data']['lots']:
                    if lot['id'] == lot_id:
                        data.append({"timestamp": row["timestamp_downloaded"].strftime("%Y-%m-%dT%H:%M:%S"),
                                     "free": lot["free"]})
            return data


def forecast(lot_id, total, date_from, date_to, version):
    if version == 1.0:
        try:
            csv_path = os.path.join(env.APP_ROOT, "forecast_data", lot_id + ".csv")

            with open(csv_path) as csvfile:
                data = {}
                for row in csv.reader(csvfile):
                    if date_from <= row[0] <= date_to:
                        data[row[0]] = row[1]
                return data
        except FileNotFoundError:
            return {}
    elif version == "1.1":
        try:
            csv_path = os.path.join(env.APP_ROOT, "forecast_data", lot_id + ".csv")

            with open(csv_path) as csvfile:
                return [{"timestamp": row[0], "free": int(total * (1 - int(row[1]) / 100))} for row in csv.reader(csvfile) if date_from <= row[0] <= date_to]
        except FileNotFoundError:
            return []
