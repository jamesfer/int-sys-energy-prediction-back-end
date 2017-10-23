from data.load import write
from data.scripts.utils import process_files, average_of


def compress_row(row):
    result = {}
    for key, value in row.items():
        if key == 'country':
            result[key] = value
            continue

        month = fix_date_key(key)[5:]
        if month in result:
            result[month] = average_of(result[month], value)
        else:
            result[month] = value
    return result


def fix_date_key(key):
    if key == 'country' or len(key) == 7:
        return key
    else:
        return key[:5] + '0' + key[-1]


def fix_date(row):
    return {fix_date_key(key): value for key, value in row.items()}


if __name__ == '__main__':
    filename_template = './data/raw_files/Monthly - %s.csv'
    years = ['1991 - 2014', '2005 - 2013', '2015']
    files = list(map(lambda year: filename_template % (year,), years))

    all_rows, keys = process_files(files, False, fix_date)
    write('./data/normalized_files/monthly.csv', all_rows, keys)

    all_rows, keys = process_files(files, False, compress_row)
    write('./data/normalized_files/monthly_compressed.csv', all_rows, keys)
