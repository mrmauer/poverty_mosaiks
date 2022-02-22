import sys
from flask import Flask, request, abort
import json

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

@app.errorhandler(422)
def missing_arguments(error):
    return ("Incorrect input. Body must be a dict with unique key 'points'"
            "and value a list of dicts with keys 'lat' and 'lon'", 422)

def get_and_validate_args():
    '''
    Expected request body:
    {"n_neighbors": 1, "points": [{"lat":10, "lon":10}, ...]}
    '''

    request_data = json.loads(request.data.decode("utf-8"))

    if 'points' not in request_data:
        abort(422)

    list_points = request_data['points']
    if not isinstance(list_points, list):
        abort(422)

    for point in list_points:
        if 'lon' not in point or 'lat' not in point:
            abort(422)

    if 'n_neighbors' in request_data:
        n = request_data['n_neighbors']
    else:
        n = 1

    return list_points, n


@app.route('/mosaiks-features/', methods=['POST'])
def mosaiks_features():

    list_points, n = get_and_validate_args()

    response = {"n_neighbors":n, "points": []}
    
    for point in list_points:
        closest_features = db.get_mosaiks_closest_features(
            lon=point['lon'],
            lat=point['lat'],
            n=n)
        response['points'].append(
            {'point': point,
             'closest_features': closest_features}
        )

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)