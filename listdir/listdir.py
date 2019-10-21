import os
import argparse
import csv
import hashlib
import zipfile
import configparser
from datetime import datetime
import logging.config
import yaml


def setup_logging(
        default_path='logging_listdir.yaml',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    """ Setup logging configuration. """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
    return 'Setting up logging.'


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
    result = hasher.hexdigest()
    return result


def zip_file(name):
    """ Zip the file under the user-defined name. """
    logging.info(f'Zipping {name}')
    with zipfile.ZipFile(f"{name}.zip", 'w', zipfile.ZIP_DEFLATED) as file:
        logging.info('Creating zip...')
        file.write(name)
    logging.info('Zipping done.')
    return f'{name}.zip'


def datetime_filename(given_name):
    """ Include the current date and time onto the specified file name. """
    logging.info(f'Naming {given_name}')
    final_name = f'{given_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    logging.info(f'Result: {final_name}')
    return final_name


def directory_files(name, files):
    """ Put the Parent Path, File Name, and File Size of files within the specified directory in a CSV file. """
    logging.info('Opened new .csv file.')
    with open(f'{name}.csv', 'w+', newline='') as csv_file:
        field_n = ['Parent Path', 'File Name', 'File Size', 'MD5', 'SHA1']
        writer = csv.DictWriter(csv_file, fieldnames=field_n)
        logging.info(f'Included the ff. headers: {field_n}.')
        writer.writeheader()
        logging.info('Writing rows...')
        for r, d, f in os.walk(files):
            for file in f:
                size = os.path.getsize(r+"//"+file)
                d = {"Parent Path": r, "File Name": file, "File Size": size,
                     "MD5": hash_file(f"{r}/{file}", 'md5'), "SHA1": hash_file(f"{r}/{file}", 'sha1')}
                writer.writerow(d)
    logging.info('Finished with .csv file. Onto zipping...')
    zip_file(f'{name}.csv')
    logging.info(f'Finished creating {name}.csv.')
    return f'{name}.csv'


def main():
    config = configparser.ConfigParser()
    o = os.path.dirname(__file__)
    config.read(o + 'config.ini')
    setup_logging()
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=config['default']['input_path'])
    parser.add_argument("name", nargs="?", default=config['default']['output_name'])
    args = parser.parse_args()
    directory_name = args.path
    logging.info(f'\nNew Log')
    output_name = datetime_filename(args.name)
    directory_files(output_name, directory_name)


if __name__ == "__main__":
    main()
