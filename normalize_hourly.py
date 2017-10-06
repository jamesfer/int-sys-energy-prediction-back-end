from data.load import read, write
from data.manipulate import merge_by

non_data_props = ['Country', 'day', 'month', 'year', 'repr']


def strip_all(row):
    return {k.strip(): v.strip() for k, v in iter(row.items())}


def extract_props(row):
    """ Takes all the actual data from the row and puts it into a subfield """
    props = {k.lower(): v for k, v in iter(row.items()) if k in non_data_props}
    data = {k: v for k, v in iter(row.items()) if k not in non_data_props}
    props['data'] = data
    return props


def clean_data(d):
    """ Returns None if d is '', '0' or 'n.a.', otherwise, converts it to an
    integer """
    return int(d) if d not in ['', '0', 'n.a.'] else None


def clean_row(row):
    """ Replaces all empty strings, zeros and 'n.a.'s in data with None """
    row['data'] = {k: clean_data(v) for k, v in iter(row['data'].items())}
    return row


def inline_date(row):
    """ Adds the year, month and date of the row to each key in data """
    date_str = '%s-%s-%s ' % (row['year'], row['month'], row['day'])
    data = {date_str + k: v for k, v in iter(row['data'].items())}
    return dict(country=row['country'], repr=row['repr'], data=data)


def normalize(row):
    """ Combines all the above functions into a single call """
    return inline_date(clean_row(extract_props(strip_all(row))))


def merge_rows(a, b):
    """ Combines the data in two rows into a single row """
    return {
        'country': b['country'],
        'repr': (int(a['repr']) + int(b['repr'])) / 2,
        'data': dict(**a['data'], **b['data'])
    }


def find_total_row(rows):
    """ Finds the sum of the data of all other rows """
    all_data = [r['data'] for r in rows]
    all_keys = {key for data in all_data for key in data}
    all_data = {
        key: sum([data[key] or 0 for data in all_data if key in data])
        for key in all_keys
    }
    return {
        'country': 'ALL',
        'repr': sum([r['repr'] for r in rows]) / len(rows),
        'data': all_data
    }


def flatten_data(row):
    return dict(country=row['country'], repr=row['repr'], **row['data'])


if __name__ == '__main__':
    all_rows = {}
    files = map(lambda year: 'Hourly - %s.csv' % (year,), range(2010, 2017))

    # Parse all of the files
    for filename in files:
        existing_rows = all_rows.values()
        new_rows = read('./data/raw_files/' + filename, map=normalize)
        all_rows = merge_by(
            'country',
            existing_rows,
            new_rows,
            merge=merge_rows)

    # Calculate all row
    all_rows['ALL'] = find_total_row(all_rows.values())

    # Flatten rows
    output_rows = list(map(flatten_data, all_rows.values()))

    # Calculate output fields
    fields = [key for row in output_rows for key in row.keys()]

    # Write results to a file
    write('./data/normalized_files/hourly.csv', output_rows, fields)
