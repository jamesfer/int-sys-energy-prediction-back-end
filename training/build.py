def build_training_set(data_set, start, end, lookback):
    filtered_data = {k: v for k, v in data_set.items() if start <= k <= end}
    filtered_keys = list(filtered_data.keys())
    key_count = len(filtered_keys)

    training_set = []
    for i in range(max(key_count - lookback, 0)):
        inputs = []
        for j in range(lookback):
            inputs.append(filtered_data[filtered_keys[i + j]])
        training_set.append(dict(
            inputs=inputs,
            output=filtered_data[filtered_keys[i + lookback]]
        ))
    return training_set
