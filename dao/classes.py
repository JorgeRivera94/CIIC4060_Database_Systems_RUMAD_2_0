import psycopg2
import os

class ClassDAO:
    def __init__(self):
        DATABASE_URL = os.environ.get("DATABASE_URL")

        self.conn = psycopg2.connect(DATABASE_URL)

    def get_all_classes(self):
        cursor = self.conn.cursor()
        query = "SELECT cid, cname, ccode, cdesc, term, years, cred, csyllabus FROM class"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)

        return result

    def get_class_by_id(self, cid):
        cursor = self.conn.cursor()
        query = "SELECT cid, cname, ccode, cdesc, term, years, cred, csyllabus FROM class WHERE cid = %s"
        cursor.execute(query, (cid,))
        result = cursor.fetchone()
        return result

    def get_class_by_name_and_code(self, cname, ccode):
        cursor = self.conn.cursor()
        query = "SELECT cid FROM class WHERE cname = %s AND ccode = %s"
        cursor.execute(query, (cname, ccode))
        result = cursor.fetchone()
        if result:
            return result[0]
        return result

    def insert_class(self, cname, ccode, cdesc, term, years, cred, csyllabus):
        cursor = self.conn.cursor()
        query = "INSERT INTO class (cname, ccode, cdesc, term, years, cred, csyllabus) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING cid"
        cursor.execute(query, (cname, ccode, cdesc, term, years, cred, csyllabus))
        cid = cursor.fetchone()[0]
        self.conn.commit()
        return cid

    def update_class_by_id(self, cid, cname, ccode, cdesc, term, years, cred, csyllabus):
        cursor = self.conn.cursor()
        query = "UPDATE class SET cname = %s, ccode = %s, cdesc = %s, term = %s, years = %s, cred = %s, csyllabus = %s WHERE cid = %s"
        cursor.execute(query, (cname, ccode, cdesc, term, years, cred, csyllabus, cid))
        rowcount = cursor.rowcount
        self.conn.commit()
        return rowcount == 1

    def delete_class_by_id(self, cid):
        cursor = self.conn.cursor()
        query = "DELETE FROM class WHERE cid = %s"
        cursor.execute(query, (cid,))
        rowcount = cursor.rowcount
        self.conn.commit()
        return rowcount == 1