import json
from flask import Flask, request, jsonify

from ann.predict import predict
from data import get_data_row, data_only
from training.build import build_training_set, denormalize

app = Flask(__name__)


@app.route('/')
def index():
    args = request.args

    # Load parameters
    country = args['country'] if 'country' in args else 'ALL'
    interval = args['interval'] if 'interval' in args else 'hourly'
    lookback = int(args['lookback']) if 'lookback' in args else 5
    start = args['start'] if 'start' in args else '2015'
    end = args['end'] if 'end' in args else '2016'

    # Build training set
    data = data_only(get_data_row(interval, country))
    training_set = build_training_set(data, start, end, lookback)

    expected_outputs = training_set['expected_outputs']
    training_inputs = training_set['training_inputs']
    training_outputs = training_set['training_outputs']
    pred_inputs = training_set['pred_inputs']
    expected_keys = training_set['expected_keys']
    low = training_set['low']
    high = training_set['high']

    # Run predictions
    results = predict(lookback,
                      training_inputs,
                      training_outputs,
                      pred_inputs)
    flat_results = [res[0] for res in results]

    predicted_outputs = denormalize(flat_results, low, high)
    expected_outputs = denormalize(expected_outputs.flatten(), low, high)

    resp = jsonify(dict(keys=expected_keys.tolist(),
                        predicted=predicted_outputs,
                        expected=expected_outputs))
    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
