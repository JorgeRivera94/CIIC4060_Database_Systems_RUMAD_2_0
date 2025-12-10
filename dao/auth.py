from config.pgconfig import pg_config
import psycopg2
import os

class AuthDAO:
    def __init__(self):
        # DATABASE_URL = os.environ.get("DATABASE_URL")
        DATABASE_URL = "dbname=%s password=%s host=%s port=%s user=%s" % \
                       (pg_config["dbname"],
                        pg_config["password"],
                        pg_config["host"],
                        pg_config["port"],
                        pg_config["user"]
                        )
        self.conn = psycopg2.connect(DATABASE_URL)

    def get_all_pairs(self):
        cursor = self.conn.cursor()
        query = """
        SELECT users.uid, username, name, pid, password
        FROM users INNER JOIN passwords ON users.uid = passwords.uid
        ORDER BY users.uid
        """
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_name_from_auth(self, username, password):
        cursor = self.conn.cursor()
        query = """
        SELECT name
        FROM users INNER JOIN passwords ON users.uid = passwords.uid
        WHERE username = %s
        AND password = %s
        """
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        if result:
            return result[0]
        return result