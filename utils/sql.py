import pymysql


class MySQL:

    def execute_query(self, connection, query):
        """
        Execute SQL query on the provided database connection.

        Parameters:
        - connection: pymysql connection object
        - query: SQL query to be executed
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        except pymysql.MySQLError as e:
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
