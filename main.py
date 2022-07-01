import datetime
import json

import requests
from flask import Flask
from flask import jsonify
from flask_caching import Cache

from config import config


def create_app(enviroment):
    app = Flask(__name__)
    return app


def create_app(enviroment):
    app = Flask(__name__)

    app.config.from_object(enviroment)

    return app

enviroment = config['development']
app = create_app(enviroment)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

ENDPOINT = "https://cat-fact.herokuapp.com/facts/random?animal_type=cat&amount="


class STATUS_HTTP:
    OK = 200
    NON_CONTENT = 204
    PARTIAL_CONTENT = 206
    ERROR = 404

@app.route('/cat-facts/<number>', methods=['GET'])
def cat_facts(number):
    response = []
    status_code = STATUS_HTTP.NON_CONTENT
    if number.isdigit() and int(number) > 0:
        number = int(number)
        if number > 500:
            response = app.response_class(response=json.dumps({'message': 'Limited to 500 facts at a time'}),
                                          status= STATUS_HTTP.OK,
                                          mimetype='application/json')
            return response
        key_cache, data_cache = get_cache_cats()
        total_cats = len(data_cache) if data_cache else 0

        if data_cache is None or total_cats < number:
            data_cache, total_cats = get_cats_facts()
            cache.set(key_cache, data_cache, timeout=3600)

        response = data_cache[:number]
        status_code = STATUS_HTTP.OK
        if number > total_cats:
            response.append({'message': F"Only {total_cats} cats facts avaible now"})
            status_code = STATUS_HTTP.PARTIAL_CONTENT

    response = app.response_class(response=json.dumps(response),
                                  status=status_code,
                                  mimetype='application/json')
    return response


def get_cache_cats():
    key_cache = "cats-facts"
    cache_data = cache.get(key_cache)
    return key_cache, cache_data


def get_cats_facts():
    valid_cats = []
    total_cats = 0
    try:
        response = requests.get(ENDPOINT+"500", timeout=10)
        if response.status_code == 200:
            json_response = json.loads(response.content)
            date_now = datetime.date.today()
            year_now = str(date_now.year)
            valid_cats = [cat for cat in json_response if cat['updatedAt'].split("-")[0] == year_now]
            total_cats = len(valid_cats)

    except(requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.ReadTimeout):
        pass

    return valid_cats, total_cats


if __name__ == '__main__':
    app.run(debug=True)


