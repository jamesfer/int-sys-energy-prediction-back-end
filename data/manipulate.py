def merge_by(prop, *arrs, merge=lambda a, b: b):
    result = {}
    for arr in arrs:
        for row in arr:
            if row[prop] in result:
                result[row[prop]] = merge(result[row[prop]], row)
            else:
                result[row[prop]] = row
    return result


def data_only(row):
    del row['country']
    del row['repr']
    return row
