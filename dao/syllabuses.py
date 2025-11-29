from config.pgconfig import pg_config
import psycopg2

class SyllabusDAO:
    def __init__(self):
        connect_url = "dbname=%s user=%s password=%s port=%d host=%s" \
                      % (pg_config["dbname"], pg_config["user"],
                         pg_config["password"], pg_config["port"], pg_config["host"])

        self.conn = psycopg2.connect(connect_url)

    def get_syllabuses_by_class_id(self, courseid):
        cursor = self.conn.cursor()
        query = "SELECT chunkid, courseid, embedding_text, chunk FROM syllabus WHERE courseid = %s"
        cursor.execute(query, (courseid,))
        result = cursor.fetchone()
        return result