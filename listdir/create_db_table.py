from listdir import psycopg2, gp, __name__ as name
import logging.config


def check_database(hostname, username):
    """Check if desired database exists. Otherwise, call a function to create desired database."""
    try:
        def_connection = psycopg2.connect(user=username,
                                          password=gp.getpass('Password: '),
                                          host=hostname,
                                          port="5433",
                                          database="postgres")
        def_connection.autocommit = True

        db_cursor = def_connection.cursor()
        check_db_query = """SELECT COUNT(*) FROM pg_catalog.pg_database
                            WHERE datname = 'listdir_db';"""
        db_cursor.execute(check_db_query)
        if db_cursor.fetchone()[0] == 0:
            create_database(db_cursor)

        db_cursor.close()
        def_connection.close()
    except Exception as e:
        logging.getLogger(name).error(f"Error in creating database - {e}")


def create_database(cursor):
    """Create the desired database."""
    try:
        query = """CREATE DATABASE listdir_db;"""
        cursor.execute(query)
    except Exception as e:
        logging.getLogger(name).error(f"Error in creating database - {e}")


def create_table(table_connection):
    """Create a table to store an ID, Parent Path, File Name, File Size, MD5 Hash and SHA1 Hash."""
    try:
        table_cursor = table_connection.cursor()
        create_table_query = """CREATE TABLE IF NOT EXISTS listdir_table(
                                ID SERIAL PRIMARY KEY NOT NULL,
                                PARENT_PATH TEXT NOT NULL,
                                FILE_NAME TEXT NOT NULL,
                                FILE_SIZE INT NOT NULL,
                                MD5 TEXT NOT NULL,
                                SHA1 TEXT NOT NULL);"""
        table_cursor.execute(create_table_query)
        table_connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.getLogger(name).error(f"Error while creating table - {error}.")
