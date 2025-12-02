from flask import jsonify
from dao.sections import SectionDAO
from dao.rooms import RoomDAO
from dao.classes import ClassDAO
from dao.meetings import MeetingDAO

class SectionHandler:
    def map_section(self, section):
        result = {}
        result["sid"] = section[0]
        result["roomid"] = section[1]
        result["cid"] = section[2]
        result["mid"] = section[3]
        result["semester"] = section[4]
        result["years"] = section[5]
        result["capacity"] = section[6]

        return result

    # GET
    def get_all_sections(self):
        dao = SectionDAO()
        sections = dao.get_all_sections()
        result = []
        for section in sections:
            result.append(self.map_section(section))
        return jsonify(result), 200

    # GET
    def get_section_by_id(self, sid):
        dao = SectionDAO()
        section = dao.get_section_by_id(sid)

        if not section:
            return jsonify(Error= "Not Found"), 404
        else:
            return jsonify(self.map_section(section)), 200

    # POST
    def insert_section(self, section_json):
        section_dao = SectionDAO()
        room_dao = RoomDAO()
        class_dao = ClassDAO()
        meeting_dao = MeetingDAO()

        roomid = cid = mid = semester = years = capacity = None
        if "roomid" in section_json:
            roomid = section_json["roomid"]
        if "cid" in section_json:
            cid = section_json["cid"]
        if "mid" in section_json:
            mid = section_json["mid"]
        if "semester" in section_json:
            semester = section_json["semester"]
        if "years" in section_json:
            years = section_json["years"]
        if "capacity" in section_json:
            capacity = section_json["capacity"]

        if (roomid and cid and mid and semester and years and capacity
                and room_dao.get_room_by_id(roomid) and class_dao.get_class_by_id(cid)
                and meeting_dao.get_meeting_by_id(mid)
                and 0 <= int(capacity) <= int(room_dao.get_room_capacity_from_id(roomid))
                and semester in {"Fall", "Spring", "V1", "V2"}
                and len(str(years)) == 4 and str(years).isnumeric()):

            if section_dao.get_section_by_room_meeting_semester_years(roomid, mid, semester, years):
                return jsonify(Error= "Conflict"), 409

            sid = section_dao.insert_section(roomid, cid, mid, semester, years, capacity)
            temp = (sid, roomid, cid, mid, semester, years, capacity)
            result = self.map_section(temp)
            return jsonify(result), 201
        else:
            return jsonify(Error= "Bad Request"), 400

    # DELETE
    def delete_section_by_id(self, sid):
        dao = SectionDAO()
        temp = dao.delete_section_by_id(sid)
        if temp:
            return jsonify(DeleteStatus= "No Content"), 204
        else:
            return jsonify(DeleteStatus= "Not Found"), 404

    # PUT
    def update_section_by_id(self, sid, section_json):
        section_dao = SectionDAO()
        room_dao = RoomDAO()
        class_dao = ClassDAO()
        meeting_dao = MeetingDAO()

        roomid = cid = mid = semester = years = capacity = None
        if "roomid" in section_json:
            roomid = section_json["roomid"]
        if "cid" in section_json:
            cid = section_json["cid"]
        if "mid" in section_json:
            mid = section_json["mid"]
        if "semester" in section_json:
            semester = section_json["semester"]
        if "years" in section_json:
            years = section_json["years"]
        if "capacity" in section_json:
            capacity = section_json["capacity"]

        if (roomid and cid and mid and semester and years and capacity
                and room_dao.get_room_by_id(roomid) and class_dao.get_class_by_id(cid)
                and meeting_dao.get_meeting_by_id(mid)
                and 0 <= int(capacity) <= int(room_dao.get_room_capacity_from_id(roomid))
                and semester in {"Fall", "Spring", "V1", "V2"}
                and len(str(years)) == 4 and str(years).isnumeric()):

            if (section_dao.get_section_by_room_meeting_semester_years(roomid, mid, semester, years)
                    and sid != section_dao.get_section_by_room_meeting_semester_years(roomid, mid, semester, years)):
                return jsonify(Error= "Conflict"), 409

            status = section_dao.update_section_by_id(sid, roomid, cid, mid, semester, years, capacity)
            if status:
                temp = (sid, roomid, cid, mid, semester, years, capacity)
                result = self.map_section(temp)
                return jsonify(result), 200
            else:
                return jsonify(Error= "Not Found"), 404
        else:
            return jsonify(Error= "Bad Request"), 400