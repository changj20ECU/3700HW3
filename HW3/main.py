from flask import Flask, render_template
import psycopg2
from psycopg2 import Error

app = Flask(__name__)

# Database connection parameters
db_config = {
    'username': 'chasecarroll',
    'password': '',
    'host': '127.0.0.1',
    'port': '5432',
    'database': 'dvdrental',
}


def connect_to_db():
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        print("Connected to the database")
        return cursor, connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)


def disconnect_from_db(connection, cursor):
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed.")
    else:
        print("Connection does not work.")


def run_and_fetch_sql(cursor, sql_string=""):
    try:
        cursor.execute(sql_string)
        record = cursor.fetchall()
        return record, ""
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return -1, error


def run_sql(cursor, sql_string=""):
    try:
        cursor.execute(sql_string)
    except (Exception, Error) as error:
        print("Error while executing PostgreSQL query", error)
        return -1, error


@app.route('/api/update_basket_a')
def update_basket_a():
    cursor, connection = connect_to_db()
    record, error = run_sql(cursor, "INSERT INTO basket_a (a, fruit_a) VALUES (5, 'Cherry');")
    connection.commit()

    if record == -1:
        print('Something is wrong with the SQL command')
        disconnect_from_db(connection, cursor)
        return "<html><body> ERROR: \n" + str(error) + "</body></html>"
    else:
        print("Success!")
        disconnect_from_db(connection, cursor)
        return "<html><body> Success! </body></html>"


@app.route('/api/unique')
def unique():
    cursor, connection = connect_to_db()
    record, error = run_and_fetch_sql(cursor,
                                      "SELECT fruit_a, fruit_b FROM basket_a FULL JOIN basket_b ON fruit_a = fruit_b WHERE a IS NULL OR b IS NULL;")

    if record == -1:
        print('Something is wrong with the SQL command')
        return "<html><body> ERROR: \n" + str(error) + "</body></html>"
    else:
        record = parse_values(record)
        col_names = [desc[0] for desc in cursor.description]
        log = record[:5]

    disconnect_from_db(connection, cursor)
    return render_template('index.html', sql_table=log, table_title=col_names)


def parse_values(record):
    results = []
    for i in range(len(record)):
        if record[i][1] is None:
            results.append((record[i][0], record[-i - 1][1]))
    return results


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1')
