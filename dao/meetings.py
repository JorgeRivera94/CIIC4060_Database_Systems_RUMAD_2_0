from config.pgconfig import pg_config
import psycopg2
import os

class MeetingDAO:
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

    def get_all_meetings(self):
        cursor = self.conn.cursor()
        query = "SELECT mid, ccode, starttime, endtime, cdays FROM meeting"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_meeting_by_id(self, mid):
        cursor = self.conn.cursor()
        query = "SELECT mid, ccode, starttime, endtime, cdays FROM meeting WHERE mid=%s"
        cursor.execute(query, (mid,))
        result = cursor.fetchone()
        return result

    def get_meeting_id_by_code(self, ccode):
        cursor = self.conn.cursor()
        query = "SELECT mid FROM meeting WHERE ccode = %s"
        cursor.execute(query, (ccode,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return result

    def insert_meeting(self, ccode, starttime, endtime, cdays):
        cursor = self.conn.cursor()
        query = "INSERT INTO meeting (ccode, starttime, endtime, cdays) VALUES (%s, %s, %s, %s) RETURNING mid"
        cursor.execute(query, (ccode,starttime,endtime,cdays))
        mid = cursor.fetchone()[0]
        self.conn.commit()
        return mid

    def update_meeting_by_id(self, mid, ccode, starttime, endtime, cdays):
        cursor = self.conn.cursor()
        query = "UPDATE meeting SET ccode = %s, starttime = %s, endtime = %s, cdays = %s WHERE mid = %s"
        cursor.execute(query, (ccode,starttime,endtime,cdays,mid))
        rowcount = cursor.rowcount
        self.conn.commit()
        return rowcount == 1

    def delete_meeting_by_id(self, mid):
        cursor = self.conn.cursor()
        query = "DELETE FROM meeting WHERE mid = %s"
        cursor.execute(query, (mid,))
        rowcount = cursor.rowcount
        self.conn.commit()
        return rowcount == 1