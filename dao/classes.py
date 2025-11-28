from config.pgconfig import pg_config
import psycopg2

class ClassDAO:
    def __init__(self):
        connect_url = "dbname=%s user=%s password=%s port=%d host=%s" \
                        %(pg_config["dbname"], pg_config["user"],
                          pg_config["password"], pg_config["port"], pg_config["host"])

        self.conn = psycopg2.connect(connect_url)

    def get_all_classes(self):
        cursor = self.conn.cursor()
        query = "SELECT cid, cname, ccode, cdesc, term, years, cred, csyllabus FROM class"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)

        return result