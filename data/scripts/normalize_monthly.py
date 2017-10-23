from data.load import write
from data.scripts.utils import process_files, average_of


def map_row(row):
    collected = {}
    for key, value in row.items():
        if key == 'country':
            collected[key] = value
            continue

        month = key[5:]
        if month in collected:
            collected[month] = average_of(collected[month], value)
        else:
            collected[month] = value
    return collected


if __name__ == '__main__':
    filename_template = './data/raw_files/Monthly - %s.csv'
    years = ['1991 - 2014', '2005 - 2013', '2015']
    files = list(map(lambda year: filename_template % (year,), years))

    all_rows, keys = process_files(files, False)
    write('./data/normalized_files/monthly.csv', all_rows, keys)

    all_rows, keys = process_files(files, False, map_row)
    write('./data/normalized_files/monthly_compressed.csv', all_rows, keys)
