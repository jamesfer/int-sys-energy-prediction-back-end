from flask import Flask, request, jsonify

import tensorflow as tf

import shutil # delete tmp directory
import os.path

from ann.predict import predict
from ann.session import modelExists
from data import get_data_row, data_only
from data.query import get_compressed_data
from training.build import build_set
from training.build_lookback import build_lookback_set, denormalize

app = Flask(__name__)

@app.route('/delete')
def delete():

    if os.path.exists('./tmp/'):
        # remove folder and its contents
        shutil.rmtree('./tmp', ignore_errors=False, onerror=None)
    
    # respond to client letting them know training data was deleted.
    resp = jsonify({'status': 'completed'})
    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/')
def index():
    settings = get_settings()
    # init the model with settings, this will setup the associated filename to load and save from.
    print(settings)

    # fixes name changes when saving/restoring model.
    tf.reset_default_graph()

    data = get_data(settings)
    training_set = get_training_set(settings, data)

    expected_outputs = training_set['expected_outputs']
    training_inputs = training_set['training_inputs']
    training_outputs = training_set['training_outputs']
    pred_inputs = training_set['pred_inputs']
    expected_keys = training_set['expected_keys']
    low = training_set['low']
    high = training_set['high']

    if len(training_inputs) == 0 or len(pred_inputs) == 0:
        resp = jsonify({'error': 'No data available for that range.'})
        resp.status_code = 400
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    # Run predictions
    results = predict(settings['train'],
                      settings['lookback'] or 1,
                      training_inputs,
                      training_outputs,
                      pred_inputs, settings)
    flat_results = [res[0] for res in results]

    predicted_outputs = denormalize(flat_results, low, high)
    expected_outputs = denormalize(expected_outputs.flatten(), low, high)

    # tells the client if the result came from a trained or untrained model.
    trained = modelExists(settings)

    resp = jsonify(dict(keys=expected_keys.tolist(),
                        predicted=predicted_outputs,
                        expected=expected_outputs,settings=settings,trained=trained))
    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


def get_settings():
    args = request.args

    train = args.get("train")
    if train == 'true':
        train = True
    elif train == 'false':
        train = False

    lookback = args.get('lookback', None)
    if lookback == 'null':
        lookback = None
    else:
        lookback = int(lookback)

    if lookback is None:
        compressed = True
    else:
        compressed = args.get('compressed', True)
    if compressed == 'true':
        compressed = True
    elif compressed == 'false':
        compressed = False

    return dict(country=(args.get('country', 'ALL')),
                interval=(args.get('interval', 'hourly')),
                start=(args.get('start', '2015')),
                end=(args.get('end', '2016')),
                compressed=compressed,
                lookback=lookback,
                train=train)


def get_data(settings):
    if settings['compressed']:
        data = get_compressed_data(settings['interval'], settings['country'])
    else:
        data = get_data_row(settings['interval'], settings['country'])
    return data_only(data)


def get_training_set(settings, data):
    if settings['lookback'] is not None:
        training_set = build_lookback_set(data, settings['start'], settings['end'], settings['lookback'])
    else:
        if settings['interval'] == 'hourly':
            if settings['compressed']:
                format_func = format_hours
            else:
                format_func = format_date
        else:
            format_func = lambda x: x
        training_set = build_set(data, settings['start'], settings['end'], format_func)
    return training_set


def date_to_num(date):
    first_sep = date.index('/')
    second_sep = date.index('/', first_sep + 1)

    year = date[:first_sep]
    month = date[first_sep + 1:second_sep]
    day = date[second_sep + 1:-9]
    hour = date[-8:-6]
    return float(year) * 365 \
           + float(month) * 31 \
           + float(day) \
           + float(hour) / 24.0


min_hourly_date = date_to_num('2010/1/20 01:00:00')
max_hourly_date = date_to_num('2016/5/18 24:00:00')


def format_date(k):
    return str((date_to_num(k) - min_hourly_date) / (max_hourly_date - min_hourly_date))


def format_hours(k):
    return str(int(k[:2]) / 24.0)
