from .load import read

hourly_data_file = './data/normalized_files/hourly.csv'


def hourly_data_for(country):
    data = read(hourly_data_file,
                filter=lambda row: row['country'] == country)
    return data[0]


def get_data_row(interval, country):
    if interval == 'hourly':
        return hourly_data_for(country)
    elif interval == 'daily':
        raise Exception('Daily interval not yet supported')
    elif interval == 'monthly':
        raise Exception('Monthly interval not yet supported')
    raise Exception('Invalid interval')
