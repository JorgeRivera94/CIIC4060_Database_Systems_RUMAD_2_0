from flask import jsonify
from dao.rooms import RoomDAO
from dao.sections import SectionDAO

class RoomHandler:
    def map_room(self, room):
        result = {}
        result["rid"] = room[0]
        result["building"] = room[1]
        result["room_number"] = room[2]
        result["capacity"] = room[3]

        return result

    # GET
    def get_all_rooms(self):
        dao = RoomDAO()
        rooms = dao.get_all_rooms()
        result = []
        for room in rooms:
            result.append(self.map_room(room))
        return jsonify(result), 200

    # GET
    def get_room_by_id(self, rid):
        dao = RoomDAO()
        room = dao.get_room_by_id(rid)

        if not room:
            return jsonify(Error="Not Found"), 404
        else:
            return jsonify(self.map_room(room)), 200

    # POST
    def insert_room(self, room_json):
        dao = RoomDAO()
        building = room_number = capacity = None
        if "building" in room_json:
            building = room_json["building"]
        if "room_number" in room_json:
            room_number = room_json["room_number"]
        if "capacity" in room_json:
            capacity = room_json["capacity"]

        if building and room_number and capacity and int(capacity) >= 0:
            if dao.get_room_by_building_and_number(building, room_number):
                return jsonify(Error="Conflict"), 409

            rid = dao.insert_room(building, room_number, capacity)
            temp = (rid, building, room_number, capacity)
            result = self.map_room(temp)
            return jsonify(result), 201
        else:
            return jsonify(Error="Bad Request"), 400

    # DELETE
    def delete_room_by_id(self, rid):
        room_dao = RoomDAO()
        section_dao = SectionDAO()

        if section_dao.get_sections_by_room_id(rid):
            return jsonify(Error="Conflict"), 409

        temp = room_dao.delete_room_by_id(rid)
        if temp:
            return jsonify(DeleteStatus= "No Content"), 204
        else:
            return jsonify(DeleteStatus= "Not Found"), 404

    # PUT
    def update_room_by_id(self, rid, room_json):
        dao = RoomDAO()
        building = room_number = capacity = None
        if "building" in room_json:
            building = room_json["building"]
        if "room_number" in room_json:
            room_number = room_json["room_number"]
        if "capacity" in room_json:
            capacity = room_json["capacity"]

        if building and room_number and capacity and int(capacity) >= 0:
            if dao.get_room_by_building_and_number(building, room_number) and rid != dao.get_room_by_building_and_number(building, room_number):
                return jsonify(Error="Conflict"), 409
            
            status = dao.update_room_by_id(rid, building, room_number, capacity)
            if status:
                temp = (rid, building, room_number, capacity)
                result = self.map_room(temp)
                return jsonify(result), 200
            else:
                return jsonify(Error="Not Found"), 404
        else:
            return jsonify(Error= "Bad Request"), 400