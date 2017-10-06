import csv


def read(filename, map=lambda x: x):
    """ Opens a csv file and reads it into a dictionary """
    with open(filename, mode='r', newline='') as infile:
        return read_from(infile, map=map)


def write(filename, rows, fields):
    """ Opens a file and writes an array of dictionaries to it """
    with open(filename, mode='w', newline='') as outfile:
        write_to(outfile, rows, fields)


def read_from(infile, map=lambda x: x):
    """ Reads a csv file into a dictionary """
    reader = csv.DictReader(infile)
    return [map(row) for row in reader]


def write_to(outfile, rows, fields):
    """ Writes an array of dictionaries to a csv file """
    writer = csv.DictWriter(outfile, fields, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(rows)
