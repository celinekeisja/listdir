import os
import argparse
import csv
import hashlib
import zipfile
import configparser
from datetime import datetime


def hash_file(file, algorithm):
    """ Hash the file using MD5 algorithm. """
    if algorithm == 'md5':
        hasher = hashlib.md5()
    elif algorithm == 'sha1':
        hasher = hashlib.sha1()
    blocksize = 65536
    with open(file, 'rb') as f:
        buf = f.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(blocksize)

    return hasher.hexdigest()


def zip_file(name):
    """ Zip the file under the user-defined name. """
    with zipfile.ZipFile(f"{name}.zip", 'w', zipfile.ZIP_DEFLATED) as file:
        file.write(name)


def datetime_filename(given_name):
    """ Include the current date and time onto the specified file name. """
    now = datetime.now()
    return f'{given_name}_{now.strftime("%Y%m%d_%H%M%S")}'


def directory_files(name, files):
    """ Put the Parent Path, File Name, and File Size of files within the specified directory in a CSV file. """
    with open(f'{name}.csv', 'w+', newline='') as csv_file:
        field_n = ['Parent Path', 'File Name', 'File Size', 'MD5', 'SHA1']
        writer = csv.DictWriter(csv_file, fieldnames=field_n)
        writer.writeheader()
        for r, d, f in os.walk(files):
            for file in f:
                size = os.path.getsize(r+"//"+file)
                d = {"Parent Path": r, "File Name": file, "File Size": size,
                     "MD5": hash_file(f"{r}/{file}", 'md5'), "SHA1": hash_file(f"{r}/{file}", 'sha1')}
                writer.writerow(d)
    zip_file(f'{name}.csv')
    return f'Created and zipped {name}.csv!'


def main():
    config = configparser.ConfigParser()
    o = os.path.dirname(__file__)
    config.read(o + '/config.ini')
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=config['default']['input_path'])
    parser.add_argument("name", nargs="?", default=config['default']['output_name'])
    args = parser.parse_args()
    directory_name = args.path
    output_name = datetime_filename(args.name)
    directory_files(output_name, directory_name)


if __name__ == "__main__":
    main()
