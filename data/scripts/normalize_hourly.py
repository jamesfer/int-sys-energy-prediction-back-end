from data.load import write
from data.scripts.utils import process_files

if __name__ == '__main__':
    filename_template = './data/raw_files/Hourly - %s.csv'
    files = list(map(lambda year: filename_template % (year,),
                     range(2010, 2017)))

    all_rows, keys = process_files(files, True)
    write('./data/normalized_files/hourly.csv', all_rows, keys)

    all_rows, keys = process_files(files, False)
    write('./data/normalized_files/hourly_compressed.csv', all_rows, keys)
