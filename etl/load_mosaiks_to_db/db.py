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
        """
    }

    def __init__(self, **config):
        self.connection = pg.connect(**config)

    def mosaiks_in_db(self, mid):
        '''
        Get all moasiks vector ids from database and return in a set
        '''
        with self.connection.cursor() as cursor:
            cursor.execute(self.SQL['MOSAIKS_IN'], (mid,))
            return len(cursor.fetchall()) > 0

        return {mosaiks_id for mosaiks_id in mosaiks_ids}

    def write_mosaiks_records(self, data):

        with self.connection.cursor() as cursor:

            for i in range(data['ids_X'].shape[0]):
                if self.mosaiks_in_db(data['ids_X'][i]):
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
