from config.pgconfig import pg_config
import psycopg2

class RoomDAO:
    def __init__(self):
        connect_url = "dbname=%s user=%s password=%s port=%d host=%s" \
                        %(pg_config["dbname"], pg_config["user"],
                          pg_config["password"], pg_config["port"], pg_config["host"])

        self.conn = psycopg2.connect(connect_url)

    def get_all_rooms(self):
        cursor = self.conn.cursor()
        query = "SELECT rid, building, room_number, capacity FROM room"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def get_room_by_id(self, rid):
        cursor = self.conn.cursor()
        query = "SELECT rid, building, room_number, capacity FROM room WHERE rid = %s"
        cursor.execute(query, (rid,))
        result = cursor.fetchone()
        return result

    def get_room_by_building_and_number(self, building, room_number):
        cursor = self.conn.cursor()
        query = "SELECT rid FROM room WHERE building = %s AND room_number = %s"
        cursor.execute(query, (building, room_number))
        result = cursor.fetchone()
        if result:
            return result[0]
        return result

    def get_room_capacity_from_id(self, rid):
        cursor = self.conn.cursor()
        query = "SELECT capacity FROM room WHERE rid = %s"
        cursor.execute(query, (rid,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return result

    def insert_room(self, building, room_number, capacity):
        cursor = self.conn.cursor()
        query = "INSERT INTO room (building, room_number, capacity) VALUES (%s, %s, %s) RETURNING rid"
        cursor.execute(query, (building, room_number, capacity))
        rid = cursor.fetchone()[0]
        self.conn.commit()
        return rid

    def update_room_by_id(self, rid, building, room_number, capacity):
        cursor = self.conn.cursor()
        query = "UPDATE room SET building = %s, room_number = %s, capacity = %s WHERE rid = %s"
        cursor.execute(query, (building, room_number, capacity, rid))
        rowcount = cursor.rowcount
        self.conn.commit()
        return rowcount == 1

    def delete_room_by_id(self, rid):
        cursor = self.conn.cursor()
        query = "DELETE FROM room WHERE rid = %s"
        cursor.execute(query, (rid,))
        rowcount = cursor.rowcount
        self.conn.commit()
        return rowcount == 1