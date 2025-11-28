import pandas as pd
from flask import jsonify
from dao.meetings import MeetingDAO
from dao.sections import SectionDAO
import datetime as dt

class MeetingHandler:
    @staticmethod
    def _fmt_time(t):
        # Accept datetime
        if isinstance(t, dt.datetime):
            t = t.isoformat(timespec='seconds')
        return t

    def map_meeting(self, meeting):
        result = {}
        result["mid"] = meeting[0]
        result["ccode"] = meeting[1]
        result["starttime"] = self._fmt_time(meeting[2])
        result["endtime"] = self._fmt_time(meeting[3])
        result["cdays"] = meeting[4]

        return result

    # GET
    def get_all_meetings(self):
        dao = MeetingDAO()
        meetings = dao.get_all_meetings()
        result = []
        for meeting in meetings:
            result.append(self.map_meeting(meeting))
        return jsonify(result), 200

    # GET
    def get_meeting_by_id(self, mid):
        dao = MeetingDAO()
        meeting = dao.get_meeting_by_id(mid)

        if not meeting:
            return jsonify(Error="NOT FOUND"), 404
        else:
            return jsonify(self.map_meeting(meeting)), 200

    # POST
    def insert_meeting(self, meeting_json):
        dao = MeetingDAO()
        ccode = starttime = endtime = cdays = None
        if "ccode" in meeting_json:
            ccode = meeting_json["ccode"]
        if "starttime" in meeting_json:
            starttime = meeting_json["starttime"]
        if "endtime" in meeting_json:
            endtime = meeting_json["endtime"]
        if "cdays" in meeting_json:
            cdays = meeting_json["cdays"]

        if ccode and starttime and endtime and cdays:
            # Validate starttime < endtime and days are MJ or LWV
            starttime = pd.to_datetime(starttime)
            endtime = pd.to_datetime(endtime)
            if (starttime >= endtime) or cdays not in {"MJ", "LWV"}:
                return jsonify(Error="Bad Request"), 400

            # Validate ccode unique
            if dao.get_meeting_id_by_code(ccode):
                return jsonify(Error="Conflict"), 409

            mid = dao.insert_meeting(ccode, starttime, endtime, cdays)
            temp = (mid, ccode, starttime, endtime, cdays)
            result = self.map_meeting(temp)
            return jsonify(result), 201
        else:
            return jsonify(Error="Bad Request"), 400

    # DELETE
    def delete_meeting_by_id(self, mid):
        meeting_dao = MeetingDAO()
        section_dao = SectionDAO()

        # Validate mid is not referenced by section
        if section_dao.get_section_by_meeting_id(mid):
            return jsonify(Error="Conflict"), 409

        temp = meeting_dao.delete_meeting_by_id(mid)
        if temp:
            return jsonify(DeleteStatus= "No Content"), 204
        else:
            return jsonify(DeleteStatus= "Not Found"), 404

    # PUT
    def update_meeting_by_id(self, mid, meeting_jason):
        dao = MeetingDAO()
        ccode = starttime = endtime = cdays = None
        if "ccode" in meeting_jason:
            ccode = meeting_jason["ccode"]
        if "starttime" in meeting_jason:
            starttime = meeting_jason["starttime"]
        if "endtime" in meeting_jason:
            endtime = meeting_jason["endtime"]
        if "cdays" in meeting_jason:
            cdays = meeting_jason["cdays"]

        if not (ccode and starttime and endtime and cdays):
            return jsonify(UpdateStatus = "Bad Request"), 400

        # Validate starttime < endtime and days are MJ or LWV
        starttime = pd.to_datetime(starttime)
        endtime = pd.to_datetime(endtime)
        if (starttime >= endtime) or cdays not in {"MJ", "LWV"}:
            return jsonify(Error="Bad Request"), 400

        # Validate ccode unique
        if dao.get_meeting_id_by_code(ccode) and mid != dao.get_meeting_id_by_code(ccode):
            return jsonify(Error="Conflict"), 409

        status = dao.update_meeting_by_id(mid, ccode, starttime, endtime, cdays)
        if status:
            temp = (mid, ccode, starttime, endtime, cdays)
            result = self.map_meeting(temp)
            return jsonify(result), 200
        else:
            return jsonify(Error="Not Found"), 404