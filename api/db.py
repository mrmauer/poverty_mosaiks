import psycopg2 as pg
from psycopg2.extras import RealDictCursor

class DB:

    SQL = {
        # SELECT features FROM mosaiks ORDER BY lonlat <-> point (%s, %s) LIMIT %s
        "GET_CLOSEST_FEATURES": """
            SELECT 
                features,
                ST_X(lonlat) AS lon,
                ST_Y(lonlat) AS lat,
                ST_Distance(
                    lonlat,
                    ST_SetSRID(ST_MakePoint(%s, %s), 4326),
                    false) AS distance
            FROM mosaiks 
            WHERE ST_DWITHIN(
                lonlat, 
                ST_SetSRID(ST_MakePoint(%s, %s), 4326),
                %s,
                false)
            ORDER BY distance
            LIMIT %s
            ;
        """
    }

    def __init__(self, **config):
        self.connection = pg.connect(**config)

    def get_mosaiks_closest_features(self, lon, lat, n=1, radius=10000):
        '''
        Get features of the max(n) closest points within radius (meters) of 
        lon/lat (SRID 4326)

        '''
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                self.SQL['GET_CLOSEST_FEATURES'],
                (lon, lat, lon, lat, radius, n))
            mosaiks_features = cursor.fetchall()

        return mosaiks_features
