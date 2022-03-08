import sys
from flask import Flask, request, abort
import json

from db import DB
from config import Config

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

@app.errorhandler(413)
def request_too_big(error):
    return ("Request size is too large. Your request must satisfy the "
            f"conditions: 'n_neighbors' <= {Config.N_NEIGHBORS_LIMIT} "
            f"and 'radius' <= {Config.RADIUS_LIMIT} and "
            f"points.length <= {Config.MAXIMUM_REQUEST_POINTS}.", 413)

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

    if len(list_points) > Config.MAXIMUM_REQUEST_POINTS:
        abort(413)

    for point in list_points:
        if 'lon' not in point or 'lat' not in point:
            abort(422)

    if 'n_neighbors' in request_data:
        n = request_data['n_neighbors']
        if n > Config.N_NEIGHBORS_LIMIT:
            abort(413)
    else:
        n = 1

    if 'radius' in request_data:
        radius = request_data['radius']
        if radius > Config.RADIUS_LIMIT:
            abort(413)
    else:
        radius = Config.DEFAULT_RADIUS

    return list_points, n, radius


@app.route('/mosaiks-features/', methods=['POST'])
def mosaiks_features():

    list_points, n, radius = get_and_validate_args()

    response = {"n_neighbors": n, "points": []}
    
    for point in list_points:
        closest_features = db.get_mosaiks_closest_features(
            lon=point['lon'],
            lat=point['lat'],
            n=n,
            radius=radius)
        response['points'].append(
            {'point': point,
             'closest_features': closest_features}
        )

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)