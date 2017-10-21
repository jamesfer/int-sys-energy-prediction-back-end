from data.load import read


def strip(row):
    """ Strips all keys and values of the row """
    return {k.strip(): v.strip() for k, v in row.items()}


def lower_keys(row):
    """ Converts all dict keys to lowercase """
    return {k.lower(): v for k, v in row.items()}


def int_values(row):
    """ Converts all values to integers if they're not None """
    return skip_keys(['country'], row,
                     lambda r: {k: int(v) if v is not None else None
                                for k, v in r.items() if k != 'country'})


def clean(row):
    """ Replaces all '', '0' and 'n.a.' with None """
    return {k: clean_value(v) for k, v in row.items()}


def clean_value(value):
    """ If value '', '0' or 'n.a.' return None otherwise returns value"""
    return value if value not in ['', '0', 'n.a.'] else None


def inline_date(row):
    """ Adds the year, month and date of the row to each key in data """
    ignore_cols = ['country', 'year', 'month', 'day']
    date_str = '%s-%s-%s ' % (row['year'], row['month'], row['day'])
    data = {date_str + k: v for k, v in row.items() if k not in ignore_cols}
    return dict(country=row['country'], **data)


def strip_cols(row):
    """ Strips all columns from the row that are not needed """
    return {k: v for k, v in row.items()
            if k not in ['repr']}


def normalize_and_inline(row):
    return int_values(inline_date(strip_cols(clean(lower_keys(strip(row))))))


def normalize(row, do_inline_date):
    return int_values(strip_cols(clean(lower_keys(strip(row)))))


def skip_keys(keys, d, action):
    skipped = {k: v for k, v in d.items() if k in keys}
    without = {k: v for k, v in d.items() if k not in keys}
    return dict(**skipped, **action(without))


def merge_dicts(*dicts, merge=lambda a, b: b, exclude=None):
    if exclude is None:
        exclude = []

    result = {}
    for d in dicts:
        for k, v in d.items():
            if k in result and k not in exclude:
                result[k] = merge(result[k], d[k])
            else:
                result[k] = d[k]
    return result


def group_collections(key, *collections, merge=lambda a, b: b):
    result = {}
    for arr in collections:
        for row in arr:
            # print(row)
            # print('\n\n\n\n')
            if row[key] in result:
                result[row[key]] = merge(result[row[key]], row)
            else:
                result[row[key]] = row
    return result.values()


def merge_rows(row_a, row_b):
    return merge_dicts(row_a, row_b, merge=lambda a, b: (a + b) / 2,
                       exclude=['country'])


def compress_row_collections(total_rows, new_rows):
    return group_collections('country', total_rows, new_rows, merge=merge_rows)


def average_of(a, b):
    if a is None or b is None:
        return None
    return (a + b) / 2


def find_average_row(all_rows):
    return merge_dicts(*all_rows, merge=average_of, exclude=['country'])
    # return skip_keys(['country'], all_rows, lambda r: merge_dicts(r))


def get_all_keys(all_rows):
    return {key for row in all_rows for key in row.keys()}


def process_files(files, do_inline_date):
    all_rows = []
    map_func = normalize_and_inline if do_inline_date else normalize
    for filename in files:
        new_rows = read(filename)
        new_rows = map(map_func, new_rows)
        all_rows = compress_row_collections(all_rows, new_rows)

    all_rows = list(all_rows)
    all_rows.append(find_average_row(all_rows))
    keys = get_all_keys(all_rows)
    return all_rows, keys
