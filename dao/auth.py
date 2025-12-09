import psycopg2
from config.pgconfig import pg_config_heroku

class AuthDAO:
    def __init__(self):
        connect_url = "dbname=%s user=%s password=%s port=%s host=%s" %(pg_config_heroku["dbname"], pg_config_heroku["user"], pg_config_heroku["password"], pg_config_heroku["port"], pg_config_heroku["host"])
        self.conn = psycopg2.connect(connect_url)

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