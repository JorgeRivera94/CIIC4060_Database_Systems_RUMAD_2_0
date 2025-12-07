import psycopg2
import os

class SyllabusDAO:
    def __init__(self):
        DATABASE_URL = os.environ.get("DATABASE_URL")

        self.conn = psycopg2.connect(DATABASE_URL)

    def get_syllabuses_by_class_id(self, courseid):
        cursor = self.conn.cursor()
        query = "SELECT chunkid, courseid, embedding_text, chunk FROM syllabus WHERE courseid = %s"
        cursor.execute(query, (courseid,))
        result = cursor.fetchone()
        return result