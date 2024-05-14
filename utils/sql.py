import pymysql
import sqlite3


class SQLite:

    def execute_query(self, connection, query):
        """
        Execute SQL query on the provided database connection.

        Parameters:
        - connection: pySQLite connection object
        - query: SQL query to be executed
        """
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error executing query: {e}")

    def __call__(self, query):
        connection = sqlite3.connect("data/restaurants.db")

        results = self.execute_query(connection, query)

        connection.close()

        return results


class SQLite:

    def execute_query(self, connection, query):
        """
        Execute SQL query on the provided database connection.

        Parameters:
        - connection: pySQLite connection object
        - query: SQL query to be executed
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        except pymysql.SQLiteError as e:
            print(f"Error executing query: {e}")

    def __call__(self, query):
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            database="restaurants",
            cursorclass=pymysql.cursors.DictCursor,
        )

        results = self.execute_query(connection, query)

        connection.close()

        return results
