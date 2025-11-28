from flask import jsonify
from dao.requisites import RequisiteDAO
from dao.classes import ClassDAO

class RequisiteHandler:
    def map_requisite(self, requisite):
        result = {}
        result["classid"] = requisite[0]
        result["reqid"] = requisite[1]
        result["prereq"] = requisite[2]

        return result

    # GET
    def get_all_requisites(self):
        dao = RequisiteDAO()
        requisites = dao.get_all_requisites()
        result = []
        for requisite in requisites:
            result.append(self.map_requisite(requisite))
        return jsonify(result), 200

    # GET
    def get_requisite_by_id(self, classid, reqid):
        dao = RequisiteDAO()
        requisite = dao.get_requisite_by_id(classid, reqid)

        if not requisite:
            return jsonify(Error="NOT FOUND"), 404
        else:
            return jsonify(self.map_requisite(requisite)), 200

    # POST
    def insert_requisite(self, requisite_json):
        requisite_dao = RequisiteDAO()
        class_dao = ClassDAO()
        classid = reqid = prereq = None
        if "classid" in requisite_json:
            classid = requisite_json["classid"]
        if "reqid" in requisite_json:
            reqid = requisite_json["reqid"]
        if "prereq" in requisite_json:
            prereq = requisite_json["prereq"]

        if classid and reqid and prereq:
            # Validate no self-requisite, unique PK pair, no cycles
            if (classid == reqid or requisite_dao.get_requisite_by_id(classid, reqid) or
                    requisite_dao.get_requisite_by_id(reqid, classid)):
                return jsonify(Error="Conflict"), 409

            # Validate FK existence
            if not (class_dao.get_class_by_id(classid) and class_dao.get_class_by_id(reqid)):
                return jsonify(Error="Not Found"), 404

            (classid, reqid) = requisite_dao.insert_requisite(classid, reqid, prereq)
            temp = (classid, reqid, prereq)
            result = self.map_requisite(temp)
            return jsonify(result), 201
        else:
            return jsonify(Error="Bad Request"), 400

    # DELETE
    def delete_requisite_by_id(self, classid, reqid):
        dao = RequisiteDAO()
        temp = dao.delete_requisite_by_id(classid, reqid)
        if temp:
            return jsonify(DeleteStatus= "No Content"), 204
        else:
            return jsonify(DeleteStatus= "Not Found"), 404