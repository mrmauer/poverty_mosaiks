import sys
from flask import Flask, request

sys.path.append('..')
from etl.load_mosaiks_to_db.db import DB
from etl.load_mosaiks_to_db.config import Config

app = Flask(__name__)

db = DB(
    dbname = Config.DATABASE_NAME,
    user = Config.DATABASE_USER,
    password = Config.DATABASE_PASSWORD,
    host = Config.DATABASE_HOST,
    port = Config.DATABASE_PORT
)

@app.route('/mosaiks-features/', methods=['GET'])
def mosaiks_features():

    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    n = request.args.get('n')

    closest_features = db.get_mosaiks_closest_features(lon=longitude, lat=latitude, n=n)

    response = {
                'closest_features':closest_features,
                'latitude': latitude,
                'longitude': longitude,
                'n': n,
                }

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)