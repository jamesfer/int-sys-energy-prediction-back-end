from .load import read

hourly_data_file = './data/normalized_files/hourly.csv'
compressed_hourly_data_file = './data/normalized_files/hourly_compressed.csv'
monthly_data_file = './data/normalized_files/monthly.csv'
compressed_monthly_data_file = './data/normalized_files/monthly_compressed.csv'


def data_for(file, country):
    data = read(file,
                filter=lambda row: row['country'] == country)
    return data[0]


def get_data_row(interval, country):
    if interval == 'hourly':
        return data_for(hourly_data_file, country)
    elif interval == 'monthly':
        return data_for
    raise Exception('Invalid interval')


def get_compressed_data(interval, country):
    if interval == 'hourly':
        return data_for(compressed_hourly_data_file, country)
    elif interval == 'monthly':
        raise Exception('Monthly interval not yet supported')
    raise Exception('Invalid interval')
