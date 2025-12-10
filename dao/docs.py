from config.pgconfig import pg_config
import psycopg2
import os

class DocDAO:
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

    def insert_doc(self, docname):
        cursor = self.conn.cursor()
        query = "INSERT INTO docs (docname) VALUES (%s) RETURNING did"
        cursor.execute(query, (docname,))
        pid = cursor.fetchone()[0]
        self.conn.commit()
        return pid