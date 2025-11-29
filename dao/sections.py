from config.pgconfig import pg_config
import psycopg2

class SectionDAO:
    def __init__(self):
        connect_url = "dbname=%s user=%s password=%s port=%d host=%s" \
                      % (pg_config["dbname"], pg_config["user"],
                         pg_config["password"], pg_config["port"], pg_config["host"])

        self.conn = psycopg2.connect(connect_url)

    def get_sections_by_meeting_id(self, mid):
        cursor = self.conn.cursor()
        query = "SELECT sid, roomid, cid, mid, semester, years, capacity FROM section WHERE mid = %s"
        cursor.execute(query, (mid,))
        result = cursor.fetchone()
        return result

    def get_sections_by_class_id(self, cid):
        cursor = self.conn.cursor()
        query = "SELECT sid, roomid, cid, mid, semester, years, capacity FROM section WHERE cid = %s"
        cursor.execute(query, (cid,))
        result = cursor.fetchone()
        return result

    def get_sections_by_room_id(self, roomid):
        cursor = self.conn.cursor()
        query = "SELECT sid, roomid, cid, mid, semester, years, capacity FROM section WHERE roomid = %s"
        cursor.execute(query, (roomid,))
        result = cursor.fetchone()
        return result