from config.pgconfig import pg_config
import psycopg2
import os

class RequisiteDAO:
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

    def get_all_requisites(self):
        cursor = self.conn.cursor()
        query = "SELECT classid, reqid, prereq FROM requisite"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_requisite_by_id(self, classid, reqid):
        cursor = self.conn.cursor()
        query = "SELECT classid, reqid, prereq FROM requisite WHERE classid = %s AND reqid = %s"
        cursor.execute(query, (classid, reqid))
        result = cursor.fetchone()
        return result

    def get_requisites_by_class_id(self, classid):
        cursor = self.conn.cursor()
        query = "SELECT classid, reqid, prereq FROM requisite WHERE classid = %s OR reqid = %s"
        cursor.execute(query, (classid, classid))
        result = cursor.fetchone()
        return result

    def insert_requisite(self, classid, reqid, prereq):
        cursor = self.conn.cursor()
        query = "INSERT INTO requisite (classid, reqid, prereq) VALUES (%s, %s, %s) RETURNING (classid, reqid)"
        cursor.execute(query, (classid, reqid, prereq))
        id = cursor.fetchone()[0]
        classid = id[1]
        reqid = id[3]
        self.conn.commit()
        return (classid, reqid)

    def delete_requisite_by_id(self, classid, reqid):
        cursor = self.conn.cursor()
        query = "DELETE FROM requisite WHERE classid = %s AND reqid = %s"
        cursor.execute(query, (classid, reqid))
        rowcount = cursor.rowcount
        self.conn.commit()
        return rowcount == 1