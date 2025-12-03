from config.pgconfig import pg_config
import psycopg2

class StatisticDAO:
    def __init__(self):
        connect_url = "dbname=%s user=%s password=%s port=%d host=%s" \
                        %(pg_config["dbname"], pg_config["user"],
                          pg_config["password"], pg_config["port"], pg_config["host"])

        self.conn = psycopg2.connect(connect_url)

    def get_sections_by_day_of_week(self, years, semester):
        cursor = self.conn.cursor()
        query = """
        SELECT section.sid, meeting.cdays
        FROM section INNER JOIN meeting ON section.mid = meeting.mid
        WHERE section.years = %s
        AND section.semester = %s
        """
        cursor.execute(query, (years, semester))
        result = []
        for row in cursor:
            result.append(row)
        return result

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

    def get_top_rooms_by_utilization(self, year, semester, limit):
        cursor = self.conn.cursor()
        query = """
        SELECT room.rid, room.building, room.room_number, avg(section.capacity ::FLOAT / room.capacity ::FLOAT) as utilization
        FROM room INNER JOIN section ON room.rid = section.roomid
        WHERE section.years = %s
        AND section.semester = %s
        GROUP BY room.rid, room.building, room.room_number
        ORDER BY avg(section.capacity ::FLOAT / room.capacity ::FLOAT) DESC
        LIMIT %s
        """
        cursor.execute(query, (year, semester, limit))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_multi_room_classes(self, year, semester, limit, orderby):
        cursor = self.conn.cursor()
        query = f"""
        SELECT class.cid, class.cname || class.ccode as fullcode, count(section.roomid)
        FROM class INNER JOIN section ON class.cid = section.cid
        WHERE section.years = %s
        AND section.semester = %s
        GROUP BY class.cid, class.cname, class.ccode
        ORDER BY count(section.roomid) {orderby}
        LIMIT %s
        """
        cursor.execute(query, (year, semester, limit))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_top_departments_by_sections(self, year, semester, limit):
        cursor = self.conn.cursor()
        query = """
        SELECT class.cname as department, count(section.sid) as sections
        FROM class INNER JOIN section ON class.cid = section.cid
        WHERE section.years = %s
        AND section.semester = %s
        GROUP BY class.cname
        ORDER BY count(section.sid) DESC
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