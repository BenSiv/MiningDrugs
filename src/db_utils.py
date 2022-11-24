"""
prapering and inserting data to SQL database
"""

import pymysql
import toml
from simple_colors import *


# Connect to the database
def connect(credentials):
    connection = pymysql.connect(
        host = credentials["host"],
        # port = int(credentials["port"]),
        user = credentials["user"],
        # password = credentials["password"],
        database = credentials["db_name"],
        charset = "utf8mb4",
        autocommit = True,
        cursorclass = pymysql.cursors.DictCursor
    )
    return connection

def send_query(query, credentials):
    connection = connect(credentials)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

def my_pretty_print(list_of_dictionaries):
    print(green("\t".join(list_of_dictionaries[0].keys()), "bold"))
    for element in list_of_dictionaries:
        list_of_values = list(element.values())
        list_of_values_string = map(str,list_of_values)
        print("\t".join(list_of_values_string))


def main(credentials_file):
    with open(credentials_file) as toml_file:
        credentials = toml.load(toml_file)

    sql = """
        SHOW TABLES;
    """
    result = send_query(sql, credentials)
    my_pretty_print(result)

if __name__ == "__main__":
    credentials_file = "/home/bensiv/Documents/ITC/Main/MySql/mysql_credentials.toml"
    main(credentials_file)
