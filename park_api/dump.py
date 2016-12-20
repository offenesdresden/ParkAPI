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
    if week and month:
        raise ValueError("Month and Week cannot be specified together.")
    if city:
        base += " city = '{0}' and".format(city)
    if not year:
        year = gmtime()[0]
    base += " extract(year from timestamp_downloaded) = '{0}'".format(year)
    if week:
        base += " and extract(week from timestamp_downloaded) = '{0}'".format(week)
    elif month:
        base += " and extract(month from timestamp_downloaded) = '{0}'".format(month)
    return base
