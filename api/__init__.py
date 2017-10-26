from flask import Flask, request, jsonify

import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
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

    if os.path.exists('./models/'):
        # remove folder and its contents
        shutil.rmtree('./models', ignore_errors=False, onerror=None)
    
    # respond to client letting them know training data was deleted.
    resp = jsonify({'status': 'deleted'})
    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/')
def index():
    settings = get_settings()
    print(settings)

    # fixes name changes when saving/restoring model.
    tf.reset_default_graph()

    data = get_data(settings)
    training_set = get_training_set(settings, data)

    training_inputs = training_set['training_inputs']
    # print('\ntraining_inputs')
    # print(training_inputs)
    training_outputs = training_set['training_outputs']
    # print('\ntraining_outputs')
    # print(training_outputs)
    pred_inputs = training_set['pred_inputs']
    # print('\nprediction_inputs')
    # print(pred_inputs)
    expected_keys = training_set['expected_keys']
    # print('\nexpected_keys')
    # print(expected_keys)
    expected_outputs = training_set['expected_outputs']
    # print('\nexpected_outputs')
    # print(expected_outputs)

    low = training_set['low']
    high = training_set['high']

    if len(training_inputs) == 0 or len(pred_inputs) == 0:
        resp = jsonify({'error': 'No data available for that range.'})
        resp.status_code = 400
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    # Run predictions

    ### Variable Descriptions ###
    ## Training ##
    # training_inputs = input values fed into the trainer = X_data > X_train
    # training_outputs = expected/goal values fed into the trainer = Y_val > Y_train
    ## Predictions ##
    # pred_inputs = input values fed into the prediction model
    # predicted_outputs = output values from the prediction

    ### TRAIN TEST SPLIT ###
    # settings['tts'] = boolean which indicates if client wants to train test split
    # randomises training data and testing data with a test size of 30%, data is shuffled
    # not feeding the same training data each time. 
    # not testing the model with same training data each time
    X_train, X_test, Y_train, Y_test = train_test_split(training_inputs, training_outputs, test_size=0.3, shuffle=True)


    if settings['tts']==True:
        # assign split train data
        training_inputs = X_train
        training_outputs = Y_train
    

    # PREDICTION
    results = predict(settings['train'],
                      settings['lookback'] or 1,
                      training_inputs,
                      training_outputs,
                      pred_inputs, settings)
    flat_results = [res[0] for res in results]


    predicted_outputs = denormalize(flat_results, low, high)
    expected_outputs = denormalize(expected_outputs.flatten(), low, high)

    # error mean squared for the prediction
    ems = mean_squared_error(expected_outputs, predicted_outputs)

    # tells the client if the result came from a trained or untrained model.
    trained = modelExists(settings)

    resp = jsonify(dict(keys=expected_keys.tolist(),
                        predicted=predicted_outputs,
                        expected=expected_outputs,settings=settings,trained=trained,
                        ems=ems))
    resp.status_code = 200
    resp.headers['Access-Control-Allow-Origin'] = '*'
    print('responded to client!')
    return resp


def get_settings():
    args = request.args

    train = args.get("train")
    if train == 'true':
        train = True
    elif train == 'false':
        train = False
    

    tts = args.get("tts")
    if tts == 'true':
        tts = True
    elif tts == 'false':
        tts = False

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
                train=train, tts=tts)


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
