#!/usr/bin/env python

import argparse
import csv
from time import gmtime

from park_api import db

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--city", help="city to dump")
    parser.add_argument("-y", "--year", help="year to dump")
    parser.add_argument("-m", "--month", help="month of year to dump")
    parser.add_argument("-w", "--week", help="week of year to dump")
    parser.add_argument("-o", "--outdir", help="output base directory")
    return parser.parse_args()

def create_query(city=None, year=None, month=None, week=None):
    base = "select city, data from parkapi where"
    count = "select count(city) from parkapi where"
    conditions = " "
    if week and month:
        raise ValueError("Month and Week cannot be specified together.")
    if city:
        conditions += "city = '{0}' and".format(city)
    if not year:
        year = gmtime()[0]
    conditions += " extract(year from timestamp_downloaded) = '{0}'".format(year)
    if week:
        conditions += " and extract(week from timestamp_downloaded) = '{0}'".format(week)
    elif month:
        conditions += " and extract(month from timestamp_downloaded) = '{0}'".format(month)
    return (base + conditions, count + conditions)

def get_data(cursor, query):
    
    cursor.execute(query[1])
    count = cursor.fetchone()['count']
    
    cursor.execute(query[0])
    table = []
    for i in range(count):
        table.append(cursor.fetchone())
    
    data = {}
    
    for row in table:
        if not row['city'] in data.keys():
            data[row['city']] = {}
        
        for lot in row['data']['lots']:
            if not lot['id'] in data[row['city']].keys():
                data[row['city']][lot['id']] = []
            data[row['city']][lot['id']].append((row['data']['last_downloaded'], lot['free']))
    
    print(data)

def main(args):
    if args.month and args.week:
        print("Month and Week cannot be specified together.")
        exit(1)
    
    query = create_query(args.city, args.year, args.month, args.week)
    
    db.setup()
    
    with db.cursor() as cursor:
        get_data(cursor, query)
    
    
    
