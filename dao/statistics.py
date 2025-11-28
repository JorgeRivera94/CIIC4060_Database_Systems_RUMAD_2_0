from config.pgconfig import pg_config
import psycopg2

class StatisticDAO:
    def __init__(self):
        connect_url = "dbname=%s user=%s password=%s port=%d host=%s" \
                        %(pg_config["dbname"], pg_config["user"],
                          pg_config["password"], pg_config["port"], pg_config["host"])

        self.conn = psycopg2.connect(connect_url)

    def define_get_duration(self):
        cursor = self.conn.cursor()
        query = """
        CREATE OR REPLACE FUNCTION get_duration(ts_start timestamp, ts_end timestamp)
            RETURNS integer
            LANGUAGE sql
            IMMUTABLE
        AS $$
        SELECT (EXTRACT(EPOCH FROM (ts_end - ts_start)) / 60)::int;
        $$;
        """
        cursor.execute(query)
        self.conn.commit()
        return True

    def get_top_classes_by_avg_duration(self, year, semester, limit):
        cursor = self.conn.cursor()
        query = """
        SELECT class.cid as cid, class.cname || class.ccode as fullcode, avg(get_duration(meeting.starttime, meeting.endtime)) as avg_minutes
        FROM class JOIN section ON class.cid = section.cid JOIN meeting ON section.mid = meeting.mid
        WHERE section.years = %s
        AND section.semester = %s
        GROUP BY class.cid
        ORDER BY avg(get_duration(meeting.starttime, meeting.endtime)) DESC, class.cid
        LIMIT %s
        """
        cursor.execute(query, (year, semester, limit))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_classes_without_prereqs(self):
        cursor = self.conn.cursor()
        query = """
        SELECT distinct cid, cname || ccode as fullcode
        FROM class
        WHERE cid NOT IN (
            SELECT class.cid
            FROM class INNER JOIN public.requisite on class.cid = requisite.classid
            )
        AND cid <> 37
        ORDER BY cid
        """
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result