from training import build_lookback_set
from data import get_data_row, data_only
from training.build import build_set

data = data_only(get_data_row('hourly', 'DE'))
# training_set = build_lookback_set(data, "2016", "2017", 3)
training_set = build_set(data)

print(training_set)
