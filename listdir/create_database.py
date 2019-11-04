from listdir import psycopg2


def database(table_connection):
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
        error_msg = f"Error while creating PostgreSQL table - {error}."
