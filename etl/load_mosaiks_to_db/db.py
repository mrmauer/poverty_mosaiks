import psycopg2 as pg
import time, sys

class DB:

    SQL = {
        "CREATE_MOSAIkS_TABLE" : """
            CREATE TABLE IF NOT EXISTS mosaiks (
                id VARCHAR(36),
                lonlat POINT,
                features REAL[],
                PRIMARY KEY (id)
            );
        """,
        "WRITE_FEATURE" : """
            INSERT INTO mosaiks (id, lonlat, features)
                VALUES (%s, Point(%s, %s), %s)
            ;
        """,
        "BUILD_RTREE" : """
            CREATE INDEX IF NOT EXISTS mosaiks_geom_idx
                ON mosaiks
                USING GIST (lonlat)
            ;
        """,
        "GET_MOSAIKS_IDS" : """
            SELECT id FROM mosaiks
            ;
        """,
        "MOSAIKS_IN" : """
            SELECT true FROM mosaiks WHERE id = %s
            ;
        """,
        "GET_CLOSEST_FEATURES": """
            SELECT features FROM mosaiks ORDER BY lonlat <-> point (%s, %s) LIMIT %s
            ;
        """
    }

    def __init__(self, **config):
        self.connection = pg.connect(**config)

    def get_mosaiks_ids(self):
        '''
        Get all moasiks vector ids from database and return in a set
        '''
        with self.connection.cursor() as cursor:
            cursor.execute(self.SQL['GET_MOSAIKS_IDS'])
            mosaiks_ids = cursor.fetchall()

        return {mosaiks_id[0] for mosaiks_id in mosaiks_ids}

    def write_mosaiks_records(self, data):

        written_ids = self.get_mosaiks_ids()

        with self.connection.cursor() as cursor:

            for i in range(data['ids_X'].shape[0]):
                if data['ids_X'][i] not in written_ids:
                    lat, lon = data['latlon'][i]
                    cursor.execute(
                        self.SQL["WRITE_FEATURE"],
                        (
                            data['ids_X'][i],
                            lon, lat,
                            data['X'][i].tolist(),
                        )
                    )
                    self.connection.commit()
                else:
                    continue

    def create_mosaiks_table(self):
        with self.connection.cursor() as cursor:
            cursor.execute(self.SQL["CREATE_MOSAIkS_TABLE"])

        self.connection.commit()


    def create_geo_index(self):
        with self.connection.cursor() as cursor:
            cursor.execute(self.SQL["BUILD_RTREE"])

        self.connection.commit()

    def get_mosaiks_closest_features(self, lon, lat, n):
        '''
        Get features of the n closest points
        '''
        with self.connection.cursor() as cursor:
            cursor.execute(self.SQL['GET_CLOSEST_FEATURES'],(lon,lat,n))
            mosaiks_features = cursor.fetchall()

        return mosaiks_features
