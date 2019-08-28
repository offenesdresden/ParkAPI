import os
import csv
from datetime import datetime

from park_api import db, env


def timespan(city, lot_id, date_from, date_to):
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    if date_from > now:
        data = forecast(lot_id, date_from, date_to)
    elif date_to < now:
        data = known_timespan_data(city, lot_id, date_from, date_to)
    else:
        data = known_timespan_data(city, lot_id, date_from, now)
        data.extend(forecast(lot_id, date_from, now))
    return data


def known_timespan_data(city, lot_id, date_from, date_to):
    with db.cursor() as cur:
        sql = '''SELECT timestamp_downloaded, data \
        FROM parkapi \
        WHERE timestamp_downloaded > %s AND timestamp_downloaded < %s AND city = %s'''
        cur.execute(sql, (date_from, date_to, city,))
        data = {}
        for row in cur.fetchall():
            for lot in row['data']['lots']:
                if lot['id'] == lot_id:
                    data[row['timestamp_downloaded'].strftime("%Y-%m-%dT%H:%M:%S")] = lot['free']
        return data


def forecast(lot_id, date_from, date_to):
    try:
        csv_path = os.path.join(env.APP_ROOT, "forecast_data", lot_id + ".csv")

        with open(csv_path) as csvfile:
            data = {}
            for row in csv.reader(csvfile):
                if date_from <= row[0] <= date_to:
                    data[row[0]] = row[1]
            return data
    except FileNotFoundError:
        return []
