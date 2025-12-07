import psycopg2
import os

class SectionDAO:
    def __init__(self):
        DATABASE_URL = os.environ.get("DATABASE_URL")

        self.conn = psycopg2.connect(DATABASE_URL)

    def get_all_sections(self):
        cursor = self.conn.cursor()
        query = "SELECT sid, roomid, cid, mid, semester, years, capacity FROM section"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_section_by_id(self, sid):
        cursor = self.conn.cursor()
        query = "SELECT sid, roomid, cid, mid, semester, years, capacity FROM section WHERE sid = %s"
        cursor.execute(query, (sid,))
        result = cursor.fetchone()
        return result

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

    def get_section_by_room_meeting_semester_years(self, roomid, mid, semester, years):
        cursor = self.conn.cursor()
        query = "SELECT sid FROM section WHERE roomid = %s AND mid = %s AND semester = %s AND years = %s"
        cursor.execute(query, (roomid, mid, semester, years))
        sid = cursor.fetchone()
        if sid:
            return sid[0]
        return sid

    def insert_section(self, roomid, cid, mid, semester, years, capacity):
        cursor = self.conn.cursor()
        query = "INSERT INTO section (roomid, cid, mid, semester, years, capacity) VALUES (%s, %s, %s, %s, %s, %s) RETURNING sid"
        cursor.execute(query, (roomid, cid, mid, semester, years, capacity))
        sid = cursor.fetchone()[0]
        self.conn.commit()
        return sid

    def update_section_by_id(self, sid, roomid, cid, mid, semester, years, capacity):
        cursor = self.conn.cursor()
        query = "UPDATE section SET roomid = %s, cid = %s, mid = %s, semester = %s, years = %s, capacity = %s WHERE sid = %s"
        cursor.execute(query, (roomid, cid, mid, semester, years, capacity, sid))
        rowcount = cursor.rowcount
        self.conn.commit()
        return rowcount == 1

    def delete_section_by_id(self, sid):
        cursor = self.conn.cursor()
        query = "DELETE FROM section WHERE sid = %s"
        cursor.execute(query, (sid,))
        rowcount = cursor.rowcount
        self.conn.commit()
        return rowcount == 1