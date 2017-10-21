from data.load import write
from data.scripts.utils import process_files

filename_template = './data/raw_files/Monthly - %s.csv'
if __name__ == '__main__':
    years = ['1991 - 2014', '2005 - 2013', '2015']
    files = map(lambda year: filename_template % (year,), years)
    all_rows, keys = process_files(files, False)
    write('./data/normalized_files/monthly.csv', all_rows, keys)
