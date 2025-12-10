from config.pgconfig import pg_config
import psycopg2
import os

class SyllabusDAO:
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

    def insert_syllabus(self, courseid, did, chunk, embedding_text):
        cursor = self.conn.cursor()
        query = "INSERT INTO syllabus (courseid, did, embedding_text, chunk) VALUES (%s, %s, %s, %s) RETURNING chunkid"
        cursor.execute(query, (courseid, did, embedding_text, chunk))
        chunkid = cursor.fetchone()[0]
        self.conn.commit()
        return chunkid

    def get_fragments(self, embedding_text):
        cursor = self.conn.cursor()
        query = "SELECT courseid, did, chunkid, chunk FROM syllabus ORDER BY embedding_text <-> %s, chunkid limit 60"
        cursor.execute(query, (embedding_text,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_fragments_by_cname_ccode(self, embedding_text, cname, ccode):
        cursor = self.conn.cursor()
        query = """
        SELECT syllabus.courseid, syllabus.did, syllabus.chunkid, syllabus.chunk 
        FROM docs INNER JOIN syllabus ON docs.did = syllabus.did INNER JOIN class ON syllabus.courseid = class.cid
        WHERE class.cname = %s
        AND class.ccode = %s
        ORDER BY embedding_text <-> %s, chunkid 
        LIMIT 15
        """
        cursor.execute(query, (cname, ccode, embedding_text))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_syllabuses_by_class_id(self, courseid):
        cursor = self.conn.cursor()
        query = "SELECT chunkid, courseid, did, embedding_text, chunk FROM syllabus WHERE courseid = %s"
        cursor.execute(query, (courseid,))
        result = cursor.fetchone()
        return result