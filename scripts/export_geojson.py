#! /usr/bin/env python

import sys
import json

import click
import psycopg2


@click.command()
@click.argument("source_name")
@click.option('-h', '--db_host', default='localhost', help='db host, defaults to localhost')
@click.option('-u', '--db_user', default='postgres', help='db user, defaults to postgres')
@click.option('-p', '--db_pass', default=None, help='db password, defaults to None')
@click.option('-o', '--db_port', default=5432, help='db port, defaults to 5432')
def main(source_name, db_host, db_user, db_pass, db_port):
    conn = psycopg2.connect(user=db_user, password=db_pass, host=db_host, port=db_port)
    cursor = conn.cursor()

    cursor.execute('SELECT name, url, source_url, has_active_support, latitude, longitude '
                   'FROM sources WHERE UPPER(name) = UPPER(%s);', (source_name,))
    source = cursor.fetchone()

    cursor.execute('SELECT l.latitude, l.longitude, l.name, l.address, l.city, l.country, l.region, l.type, '
                   'l.has_forecast, l.detail_url, l.total_spaces, l.pricing, l.opening_hours, l.additional_info '
                   'FROM lots l JOIN sources ON l.source_id = sources.id '
                   'WHERE UPPER(sources.name) = UPPER(%s) ORDER BY l.id;', (source_name, ))
    rows = cursor.fetchall()

    geojson = {
        'type': 'FeatureCollection',
        'properties': {
            'name': source[0],
            'url': source[1],
            'source_url': source[2],
            'active_support': source[3]
        },
        'features': []
    }

    for row in rows:
        lat, lng = row[0], row[1]
        if not lat:
            print(f'no geodata available for {row[2]}, skipping for geojson generation', file=sys.stderr)
            continue

        (name, address, city, country, region, lot_type, has_forecast,
         detail_url, total_spaces, pricing, opening_hours, additional_info) = row[2:]

        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [
                    lng,
                    lat
                ]
            },
            'properties': {
                'name': name,
                'address': address,
                'city': city,
                'country': country,
                'region': region,
                'type': lot_type,
                'has_forecast': has_forecast,
                'detail_url': detail_url,
                'total_spaces': total_spaces,
                'pricing': pricing,
                'opening_hours': opening_hours,
                'additional_info': additional_info
            }
        }
        geojson['features'].append(feature)

    geojson = json.dumps(geojson, indent=2, ensure_ascii=False)
    print(geojson)


if __name__ == '__main__':
    main()
