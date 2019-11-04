import configparser

import psycopg2
import os

config = configparser.ConfigParser()
o = os.path.dirname(__file__)
config.read(o + '/config.ini')
print(config)
try:
    connection = psycopg2.connect(user=config['db']['username'],
                                  password="password",
                                  host=config['db']['hostname'],
                                  port="5433",
                                  database="listdir_db")
    print(connection)

    print(connection.get_dsn_parameters(), "\n")
except Exception as e:
   print(f"Error in connection - {e}")
