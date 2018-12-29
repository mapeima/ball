import pymysql.cursors


class DBCOnnection:
    """Wrapper class for persistant database connection.

    Atributes:
        connection (pymysql.connections.Connection): The connection object to connect to the database.
        cursor (pymysql.cursors.Cursor): The cursor object to execute statements to the database.
    """

    def __init__(self):
        """Connects to the database and creates a cursor for executing statements.
        """
        self.connection = pymysql.connect(host='10.10.10.100', user='root', password='75bfd277db', db='ball',
                                          charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()

    def execute(self, sql, *args):
        """Executes the statement passed as argument and returns the result of the execution, in case of error executes
            rollback.

        Args:
            sql (str): The sql statement to be executed.

        Returns:
            list:The rows fetched when the statement is executed.

        """
        try:
            self.cursor.execute(sql, args)

            result = self.cursor.fetchall()

            self.connection.commit()

            return result

        except Exception as e:
            self.connection.rollback()

            raise e
