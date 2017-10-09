from .load import read

hourly_data_file = './normalized_files/hourly.csv'


def hourly_data_for(country):
    data = read(hourly_data_file, filter=lambda row: row['country'] == country)
    data.pop('country', None)
    data.pop('repr', None)
    return data


def get_raw_data(interval, country):
    if interval == 'hourly':
        return hourly_data_for(country)
    elif interval == 'daily':
        raise Exception('Daily interval not yet supported')
    elif interval == 'monthly':
        raise Exception('Monthly interval not yet supported')
    raise Exception('Invalid interval')
