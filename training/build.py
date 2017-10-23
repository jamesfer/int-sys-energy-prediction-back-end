import numpy as np

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


def wrap_array(values):
    return list(map(lambda x: [x], values))
