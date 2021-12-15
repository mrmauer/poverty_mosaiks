from db import DB
from config import Config
import pickle


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
db.connection.close()

print("FIN")
