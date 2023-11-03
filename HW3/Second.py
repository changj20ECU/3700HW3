import psycopg2
from psycopg2 import Error


def connect_to_db(username='raywu1990', password='test', host='127.0.0.1', port='5432', database='dvdrental'):
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user=username, password=password, host=host, port=port, database=database)
        cursor = connection.cursor()
        print("Connected to the database")
        return cursor, connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return None, None


def disconnect_from_db(connection, cursor):
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
    else:
        print("Connection does not work")


def run_and_fetch_sql(cursor, sql_string=""):
    try:
        cursor.execute(sql_string)
        record = cursor.fetchall()
        return record, ""
    except (Exception, Error) as error:
        print("Error while executing PostgreSQL query", error)
        return -1, error


def run_sql(cursor, sql_string=""):
    try:
        cursor.execute(sql_string)
    except (Exception, Error) as error:
        print("Error while executing PostgreSQL query", error)
        return -1, error


if __name__ == '__main__':
    cursor, connection = connect_to_db()

    if cursor is not None:
        # Example: Run SQL query
        sql_query = "SELECT * FROM your_table;"
        result, error = run_and_fetch_sql(cursor, sql_query)

        if result != -1:
            print("Query result:", result)

        disconnect_from_db(connection, cursor)
    else:
        print("Database connection failed.")
