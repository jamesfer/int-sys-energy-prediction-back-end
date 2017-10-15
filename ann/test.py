from training import build_training_set
from data import get_data_row

data = get_data_row('hourly', 'ALL')
training_set = build_training_set(data, "2016", "2017", 3)

print(training_set)
