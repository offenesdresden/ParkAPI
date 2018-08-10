CREATE TABLE sources (
  id serial PRIMARY KEY,
  name text NOT NULL UNIQUE,
  attribution_contributor text,
  attribution_license text,
  attribution_url text,
  url text,
  source_url text NOT NULL,
  latitude double precision,
  longitude double precision,
  has_active_support boolean NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone NOT NULL -- TODO: automatically update these via triggers
);

CREATE TYPE lot_type AS ENUM ('underground', 'lot', 'carpark');

CREATE TABLE lots (
  id serial PRIMARY KEY,
  name text NOT NULL,
  address text,
  region text,
  city text,
  country text,
  -- coordinates geography, -- is this an option via postgis?
  latitude double precision,
  longitude double precision,
  type lot_type,
  has_forecast boolean NOT NULL,
  detail_url text,
  total_spaces integer,
  source_id integer NOT NULL,
  FOREIGN KEY (source_id) REFERENCES sources(id),
  pricing text,
  opening_hours text,
  additional_info text,
  created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone NOT NULL -- TODO: automatically update these via triggers
);

CREATE TYPE lot_state AS ENUM ('open', 'closed', 'no_data');

CREATE TABLE data (
  id serial PRIMARY KEY,
  lot_id integer NOT NULL,
  FOREIGN KEY (lot_id) REFERENCES lots(id),
  free_count integer NOT NULL,
  total_count integer,
  state lot_state,
  timestamp_downloaded timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  timestamp_data_age timestamp with time zone
);

CREATE TABLE pools (
  id serial PRIMARY KEY,
  name text NOT NULL UNIQUE,
  type text,
  created_at timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp with time zone NOT NULL -- TODO: automatically update these via triggers
);

CREATE TABLE pools_lots (
  pool_id integer,
  lot_id integer,
  FOREIGN KEY (pool_id) REFERENCES pools(id),
  FOREIGN KEY (lot_id) REFERENCES lots(id),
  PRIMARY KEY (pool_id, lot_id)
);

-- Materialized Data Views, create one for each city/data-source

CREATE MATERIALIZED VIEW data_dresden AS SELECT DISTINCT ON (lots.id)
    lots.id, lots.name, data.timestamp_downloaded, data.timestamp_data_age, data.state, data.free_count, data.total_count
FROM
    lots
    JOIN data ON lots.id = data.lot_id
    WHERE lots.city = 'Dresden'
ORDER BY
    lots.id, data.timestamp_downloaded DESC;

CREATE UNIQUE INDEX lot_id ON data_dresden (id); -- create unique indices so that refreshing can be done concurrently

-- REFRESH MATERIALIZED VIEW CONCURRENTLY data_dresden;

