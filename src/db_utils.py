"""
prapering and inserting data to SQL database
"""

import pymysql
import toml
from simple_colors import *


# Connect to the database
def connect(credentials):
    """connects to the database"""
    connection = pymysql.connect(
        host = credentials["host"],
        port = int(credentials["port"]),
        user = credentials["user"],
        # password = credentials["password"],
        database = credentials["db_name"],
        charset = "utf8mb4",
        autocommit = True,
        cursorclass = pymysql.cursors.DictCursor
    )
    return connection

def send_query(query, connection):
    """sends a query to database and returns results"""
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()

def my_pretty_print(list_of_dictionaries):
    """pretty print a dictionary from sql query result"""
    print(green("\t".join(list_of_dictionaries[0].keys()), "bold"))
    for element in list_of_dictionaries:
        list_of_values = list(element.values())
        list_of_values_string = map(str,list_of_values)
        print("\t".join(list_of_values_string))

def get_column_names(table, connection):
    column_names_query = f"""
        SELECT COLUMN_NAME
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = 'drugs' 
        AND TABLE_NAME = "{table}";
    """
    column_names = [column["COLUMN_NAME"] for column in send_query(column_names_query, connection)]
    return column_names

def increment_id(table, connection):
    next_id_query = f"""
        SELECT AUTO_INCREMENT
        FROM information_schema.TABLES
        WHERE TABLE_SCHEMA = 'drugs'
        AND TABLE_NAME = "{table}";
    """
    next_id = send_query(next_id_query, connection)[0]["AUTO_INCREMENT"]
    return next_id

def get_id(table, obj, connection):
    column_name = table[:-1] + "_name"
    query = f"""
        SELECT id
        FROM {table}
        WHERE {column_name}="{obj.name}"
    """
    name_id = send_query(query, connection)
    if len(name_id) > 0:
        return name_id[0]["id"]

def main(credentials_file):
    """checks the connaction"""
    with open(credentials_file) as toml_file:
        credentials = toml.load(toml_file)

    sql = """
        SHOW TABLES;
    """
    connection = connect(credentials)
    result = send_query(sql, connection)
    my_pretty_print(result)

if __name__ == "__main__":
    credentials_file = "/home/bensiv/Documents/ITC/Main/MySql/mysql_credentials.toml"
    main(credentials_file)
