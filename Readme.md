## Setup

### Using API

Example request:
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"n_neighbors":2, "points":[{"lat":10, "lon":10}, {"lat":15, "lon":20}]}' \
  http://127.0.0.1:5000/mosaiks-features/
```

### Accessing psql

Command to psql on AWS: [here](https://harriscapp.slack.com/archives/D012DNQDH45/p1639690455006800)

.env used by python scripts should have the following:

```
#!/bin/bash
export MOSAIKS_DATABASE_PASSWORD=<password_here>
export MOSAIKS_DATABASE_HOST=<db_host_here>
```

### Start psql server locally:

`pg_ctl -D /usr/local/var/postgres start`

## SQL commands to find the closest points:

#### If using geo Index

To query for all features (and their exact lon/lat)  within 10000 meters (ie 10 km) of an input longitude/latitude:

`SELECT features, ST_X(lonlat) x, ST_Y(lonlat) y FROM mosaiks WHERE ST_DWITHIN(lonlat, ST_SetSRID(ST_MakePoint(<INPUT_LONGITUDE>, <INPUT_LATITUDE>), 4326), 10000, false)`

Documentation for everything used:
https://postgis.net/docs/ST_DWithin.html
https://postgis.net/docs/ST_SetSRID.html
https://postgis.net/docs/ST_MakePoint.html

Alternatively, if you're down with string injections, you can also do it with less postgis functions:

`SELECT features, ST_X(lonlat) x, ST_Y(lonlat) y FROM mosaiks WHERE ST_DWITHIN(lonlat, 'SRID=4326;POINT(<INPUT_LONGITUDE> <INPUT_LATITUDE>)', 10000, false)`

#### If using GiST index

`SELECT lonlat FROM mosaiks ORDER BY lonlat <-> point (<INPUT_LONGITUDE>, <INPUT_LATITUDE>) LIMIT 1;`

