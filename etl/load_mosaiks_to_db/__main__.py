from db import DB
from config import Config
import pickle

point_lon = -74.013
pont_lat = 40.711
n = 1

db = DB(
    dbname = Config.DATABASE_NAME,
    user = Config.DATABASE_USER,
    password = Config.DATABASE_PASSWORD,
    host = Config.DATABASE_HOST,
    port = Config.DATABASE_PORT
)

with open('../data/WORLD_UAR.pkl', 'br') as f:
    data = pickle.load(f)

db.create_mosaiks_table()
db.write_mosaiks_records(data)
db.create_geo_index()
closest_features = db.get_mosaiks_closest_features(point_lon, pont_lat, n)
db.connection.close()

print("FIN")
