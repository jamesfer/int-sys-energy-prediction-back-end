import numpy as np


def build_training_set(data_set, start, end, lookback):
    data_set = convert_to_int(data_set)
    data_set = {k: v for k, v in data_set.items() if v is not None}

    data_set, low, high = normalize(data_set)
    inputs, outputs, keys = extract_training_set(data_set, lookback)
    all_keys, all_inputs, all_outputs,  = segment(keys, inputs, outputs,
                                                  start=start, end=end)
    exp_keys = all_keys[0]
    pred_inputs, train_inputs = all_inputs
    exp_outputs, train_outputs = all_outputs

    return dict(
        training_inputs=np.array(train_inputs),
        training_outputs=np.array(train_outputs),
        expected_keys=np.array(exp_keys),
        expected_outputs=np.array(exp_outputs),
        pred_inputs=np.array(pred_inputs),
        low=low,
        high=high,
    )


def filter_range(data_set, end, start):
    included = {k: int_or_none(v) for k, v in data_set.items()
                if start <= k <= end}
    excluded = {k: int_or_none(v) for k, v in data_set.items()
                if k < start or k > end}
    return included, excluded


def int_or_none(value):
    return None if value == '' else int(value)


def convert_to_int(data_set):
    return {k: int_or_none(v) for k, v in data_set.items()}


def normalize(data):
    low = min(data.values())
    high = max(data.values())
    return {k: (v - low) / (high - low) if v is not None else None
            for k, v in data.items()}, low, high


def denormalize(data, high, low):
    return [v * (high - low) + low for v in data]


def extract_training_set(data, lookback):
    keys = list(data.keys())
    set_count = max(len(keys) - lookback, 0)
    all_inputs = []
    all_outputs = []
    output_keys = []

    for i in range(set_count):
        input_data = [data[keys[i + j]] for j in range(lookback)]
        output_data = [data[keys[i + lookback]]]

        if all(input_data) and all(output_data):
            all_inputs.append(np.array(input_data))
            all_outputs.append(np.array(output_data))
            output_keys.append(keys[i + lookback])
    return all_inputs, all_outputs, output_keys


def segment(keys, inputs, outputs, start='', end=''):
    indexes = [index for index, key in enumerate(keys) if start <= key <= end]

    def _filter(arr):
        included = [val for ind, val in enumerate(arr) if ind in indexes]
        excluded = [val for ind, val in enumerate(arr) if ind not in indexes]
        return included, excluded
    return _filter(keys), _filter(inputs), _filter(outputs)
