import numpy as np
from datetime import datetime, timedelta

from training.build_lookback import convert_to_num, normalize, num_or_none


def build_set(data_set, start, end, format_keys=lambda x: x):
    data_set = convert_to_num(data_set)
    data_set = {k: v for k, v in data_set.items() if v is not None}

    data_set, low, high = normalize(data_set)
    expected = {k: v for k, v in data_set.items() if start <= k <= end}

    train_inputs = map(format_keys, data_set.keys())
    train_inputs = map(num_or_none, train_inputs)
    pred_inputs = map(format_keys, expected.keys())
    pred_inputs = map(num_or_none, pred_inputs)

    return dict(
        training_inputs=np.array(wrap_array(train_inputs)),
        training_outputs=np.array(wrap_array(data_set.values())),
        expected_keys=np.array(list(expected.keys())),
        expected_outputs=np.array(wrap_array(expected.values())),
        pred_inputs=np.array(wrap_array(pred_inputs)),
        high=high,
        low=low
    )

def build_future_set(settings):
    # a future set, you don't want any training data, just want to return the correct input values
    if settings['interval']=='hourly':
        # generates a list of datetimes associated to hours requested to addon
        future_from_dates_keys = generateFutureHoursKeys(settings['futureFromHours'])
        print(len(future_from_dates_keys))
        future_from_dates_values = generateFutureHoursValues(future_from_dates_keys)
        # return future set
        return dict(
            future_pred_input_values=np.array(wrap_array(future_from_dates_values)),
            future_pred_input_keys=np.array(future_from_dates_keys),
            high=date_to_num(future_from_dates_keys[-1]),
            low=date_to_num(future_from_dates_keys[0])
        )

def generateFutureHoursKeys(hoursToAdd):
    # returns future prediction keys
    # get datetime now in YYYY/MM/DD HH:00:00 format
    fromDateKeys = []

    hoursRange = int(hoursToAdd) + 1
    for x in range(0, hoursRange):
        date = fixDateHour(hours=x)
        key = date
        fromDateKeys.append(key)

    return fromDateKeys



def generateFutureHoursValues(keys):
    min_hourly_date = date_to_num(keys[0])
    max_hourly_date = date_to_num(keys[-1])

    values = []
    keyRange = int(len(keys))
    for x in range(0, keyRange):
        value = str((date_to_num(keys[x]) - min_hourly_date) / (max_hourly_date - min_hourly_date))
        values.append(value)

    print(min_hourly_date)
    print(max_hourly_date)
    return values

def fixDateHour(hours):
    # datetime uses 0-23 range, our dataset uses 1-24 range for hours
    # get datetime from now + hours
    date = datetime.now().replace(microsecond=0, minute=0, second=0) + timedelta(hours=hours)
    if (date.hour==0):
        # subtract a day
        date = date - timedelta(hours=24)
        # change to string, change HH to 24
        date = list(str(date))
        date[11] = '2'
        date[12] = '4'
        date = ''.join(date)

    # return string
    return str(date).replace("-", "/")

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

def format_date(k):
    print(date_to_num(k))
    return str((date_to_num(k) - min_hourly_date) / (max_hourly_date - min_hourly_date))

def get_date_hour(date):
    return date[-8:-6]

def format_hours(k):
    return str(int(k[:2]) / 24.0)

def wrap_array(values):
    return list(map(lambda x: [x], values))
