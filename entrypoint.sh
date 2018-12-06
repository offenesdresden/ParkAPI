#!/bin/sh

if [ -z $port ]; then
  port="5000"
fi

if [ -z $host ]; then
  host="::1"
fi

if [ -z $debug ]; then
  debug="false"
fi

if [ -z $live_scrape ]; then
  live_scrape="true"
fi

if [ -z $database_uri ]; then
  database_uri="postgresql://$PGUSER:$PGPASS@$PGHOST/$PGDATABASE"
fi

echo "
[DEFAULT]
port = $port
host = $host
debug = $debug
live_scrape = $live_scrape
database_uri = $database_uri
[development]
port = $port
host = $host
debug = $debug
live_scrape = $live_scrape
database_uri = $database_uri
" > /app/config.ini

python bin/parkapi-server
