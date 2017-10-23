from data.load import read


def strip(row):
    """ Strips all keys and values of the row """
    return {k.strip(): v.strip() for k, v in row.items()}


def lower_keys(row):
    """ Converts all dict keys to lowercase """
    return {k.lower(): v for k, v in row.items()}


def num_values(row):
    """ Converts all values to integers if they're not None """
    return skip_keys(['country'], row,
                     lambda r: {k: float(v) if v is not None else None
                                for k, v in r.items() if k != 'country'})


def clean(row):
    """ Replaces all '', '0' and 'n.a.' with None """
    return {k: clean_value(v) for k, v in row.items()}


def clean_value(value):
    """ If value '', '0' or 'n.a.' return None otherwise returns value"""
    return value if value not in ['', '0', 'n.a.'] else None


def strip_cols(row, do_inline_date):
    """ Strips all columns from the row that are not needed """
    ignore_cols = ['country', 'year', 'month', 'day', 'sum', 'repr']
    if do_inline_date:
        date_str = '{}/{:0>2}/{} '.format(row['year'], row['month'], row['day'])
    else:
        date_str = ''
    data = {date_str + k: v for k, v in row.items() if k not in ignore_cols}
    return dict(country=row['country'], **data)


def normalize_and_inline(row):
    return num_values(strip_cols(clean(lower_keys(strip(row)))))


def normalize(row, do_inline_date):
    return num_values(strip_cols(clean(lower_keys(strip(row))), do_inline_date))


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
    return merge_dicts(row_a, row_b, merge=average_of,
                       exclude=['country'])


def compress_row_collections(total_rows, new_rows):
    return group_collections('country', total_rows, new_rows, merge=merge_rows)


def average_of(*nums):
    return sum([0 if num is None else num for num in nums]) / 2


def find_average_row(all_rows):
    return merge_dicts(*all_rows, merge=average_of, exclude=['country'])


def get_all_keys(all_rows):
    keys = list({key for row in all_rows for key in row.keys()})
    keys.sort()
    keys.pop()
    keys.insert(0, 'country')
    return keys


# def map_keys(rows, func):
#     return map(lambda row: skip_keys('country', row,
#                                      lambda r: {func(k): v
#                                                 for k, v in r.items()}),
#                rows)


def process_files(files, do_inline_date):
    all_rows = []
    for filename in files:
        new_rows = read(filename)
        new_rows = map(lambda row: normalize(row, do_inline_date), new_rows)
        # new_rows = map_keys(new_rows, format_key)

        all_rows = compress_row_collections(all_rows, new_rows)

    all_rows = list(all_rows)
    all_rows.append(find_average_row(all_rows))
    keys = get_all_keys(all_rows)
    return all_rows, keys
