import argparse
import configparser
import csv
import getpass as gp
import hashlib
import json
import logging.config
import os
import zipfile
from datetime import datetime
import psycopg2
import yaml
import create_db_table
import pika


def send_to_queue(hostname, queue_name, routing_key, files):
    """Connects to queue and sends file information in json format."""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=hostname))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    try:
        for r, d, f in os.walk(files):
            for file in f:
                i = json.dumps(json_rows(r, file))
                channel.basic_publish(exchange='',
                                      routing_key=routing_key,
                                      body=i)
                logging.info("[x] Sent {} to queue!".format(i))
        return "[x] Sent!"
    except:
        logger.error("Unable to json.")
    connection.close()


def database_connection(hostname, username, port, database):
    """Connects to the database."""
    try:
        connection = psycopg2.connect(user=username,
                                      password=gp.getpass('Password: '),
                                      host=hostname,
                                      port=port,
                                      database=database)
        return connection
    except Exception as e:
        logger.error(f"Error in connection - {e}")


def database_insert(connection, files):
    """Inserts records of files in a database."""
    try:
        cursor = connection.cursor()
        try:
            for r, d, f in os.walk(files):
                for file in f:
                    size = os.path.getsize(r + os.sep + file)
                    path = os.path.abspath(r + os.sep + file)
                    insert_query = """INSERT INTO listdir_table 
                    (PARENT_PATH, FILE_NAME, FILE_SIZE, MD5, SHA1) 
                    VALUES (%s, %s, %s, %s, %s);"""
                    record_to_insert = (path, file, size, hash_file(f"{r}{os.sep}{file}", 'md5'), hash_file(f"{r}{os.sep}{file}", 'sha1'))
                    cursor.execute(insert_query, record_to_insert)
                    connection.commit()
        except (Exception, psycopg2.Error) as error:
            logger.error(f"Unable to insert record - {error}")
    except (Exception, psycopg2.Error) as error:
        logger.error(error)
    finally:
        if connection:
            cursor.close()
            connection.close()


def setup_logging(default_path='logging_listdir.yaml',
                  default_level=logging.INFO,
                  env_key='LOG_CFG'):
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


def json_rows(r, file):
    size = os.path.getsize(r + os.sep + file)
    path = os.path.abspath(r + os.sep + file)
    data = {}
    data[file] = []
    data[file].append({
        'Parent Path': path,
        'File Name': file,
        'File Size': size,
        'MD5': hash_file(path, 'md5'),
        'SHA1': hash_file(path, 'sha1')
    })
    return data


def json_files(name, files):
    """ Put the Parent Path, File Name, and File Size of files within the specified directory in a JSON file. """
    logger.info('Opening new .json file.')
    try:
        with open(f'{name}.json', 'w+', newline='') as json_file:
            logger.info('Writing rows...')
            try:
                for r, d, f in os.walk(files):
                    for file in f:
                        json.dump(json_rows(r, file), json_file, indent=2)
            except:
                logger.error("Unable to write file.")
    except:
        logger.error('Unable to write a new file.')
    logger.info('Finished with .json file. Onto zipping...')
    return f'{name}.json'


def hash_file(file, algorithm):
    """ Hash the file using MD5 algorithm. """
    if algorithm == 'md5':
        hasher = hashlib.md5()
    elif algorithm == 'sha1':
        hasher = hashlib.sha1()
    blocksize = 65536
    try:
        with open(file, 'rb') as f:
            buf = f.read(blocksize)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(blocksize)
        result = hasher.hexdigest()
    except:
        logger.error('Unable to Hash.')
    return result


def zip_file(name):
    """ Zip the file under the user-defined name. """
    logger.info(f'Zipping {name}')
    try:
        with zipfile.ZipFile(f"{name}.zip", 'w', zipfile.ZIP_DEFLATED) as file:
            logger.info('Creating zip...')
            file.write(name)
    except:
        logger.error('An error occurred while zipping.')
    logger.info('Zipping done.')
    return f'{name}.zip'


def datetime_filename(given_name):
    """ Include the current date and time onto the specified file name. """
    logger.info(f'Naming {given_name}')
    try:
        final_name = f'{given_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    except:
        logger.error('Unable to name properly.')
    logger.info(f'Result: {final_name}')
    return final_name


def csv_files(name, files):
    """ Put the Parent Path, File Name, and File Size of files within the specified directory in a CSV file. """
    logger.info('Opening new .csv file.')
    try:
        with open(f'{name}.csv', 'w+', newline='') as csv_file:
            field_n = ['Parent Path', 'File Name', 'File Size', 'MD5', 'SHA1']
            writer = csv.DictWriter(csv_file, fieldnames=field_n)
            logger.info(f'Including the ff. headers: {field_n}.')
            try:
                writer.writeheader()
            except:
                logger.error('Unable to write header.')
            logger.info('Writing rows...')
            try:
                for r, d, f in os.walk(files):
                    for file in f:
                        path = os.path.abspath(r + os.sep + file)
                        size = os.path.getsize(path)
                        d = {"Parent Path": path, "File Name": file, "File Size": size,
                             "MD5": hash_file(f"{path}", 'md5'),
                             "SHA1": hash_file(f"{path}", 'sha1')}
                        writer.writerow(d)
            except:
                logger.error("Unable to write file.")
    except:
        logger.error('Unable to write a new file.')
    logger.info('Finished with .csv file. Onto zipping...')
    return f'{name}.csv'


def main():
    """ Main function """
    config = configparser.ConfigParser()
    o = os.path.dirname(__file__)
    p = o + 'config.ini'
    config.read(o + 'config.ini')
    setup_logging()
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=config['default']['input_path'])
    parser.add_argument("name", nargs="?", default=config['default']['output_name'])
    parser.add_argument("-j", "--json", action="store_true")
    parser.add_argument("-c", "--csv", action="store_true")
    parser.add_argument("-d", "--db", action="store_true")
    parser.add_argument("-q", "--queue", action="store_true")
    args = parser.parse_args()
    directory_name = args.path
    try:
        if args.db:
            try:
                hostname = config['db']['hostname']
                username = config['db']['username']
                create_db_table.check_database(hostname, username)
                connection = database_connection(hostname, username, config['db']['port'], config['db']['database'])
                create_db_table.create_table(connection)
                database_insert(connection, directory_name)
            except Exception as e:
                logger.error(f"Error in DB - {e}")
            logger.info(f'Finished inserting records.')
        else:
            output_name = datetime_filename(args.name)
            if args.json:
                try:
                    new_name = zip_file(json_files(output_name, directory_name))
                except:
                    logger.error('Unable to zip file.')
                logger.info(f'Finished creating {new_name}.')
            elif args.csv:
                try:
                    new_name = zip_file(csv_files(output_name, directory_name))
                except:
                    logger.error('Unable to zip file.')
                logger.info(f'Finished creating {new_name}.')
            elif args.queue:
                try:
                    hostname = config['queue']['hostname']
                    queue_name = config['queue']['queue_name']
                    routing_key = config['queue']['routing_key']
                    send_to_queue(hostname, queue_name,
                                  routing_key, directory_name)
                except:
                    logger.error('Unable to send to queue!')
    except:
        logger.error('Did not specify type.')


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    main()
