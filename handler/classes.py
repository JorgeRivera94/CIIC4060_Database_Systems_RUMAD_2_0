from flask import jsonify
from dao.classes import ClassDAO
from dao.requisites import RequisiteDAO
from dao.syllabuses import SyllabusDAO
from dao.sections import SectionDAO

class ClassHandler:
    def map_class(self, c):
        result = {}
        result["cid"] = c[0]
        result["cname"] = c[1]
        result["ccode"] = c[2]
        result["cdesc"] = c[3]
        result["term"] = c[4]
        result["years"] = c[5]
        result["cred"] = c[6]
        result["csyllabus"] = c[7]

        return result

    # GET
    def get_all_classes(self):
        dao = ClassDAO()
        classes = dao.get_all_classes()
        result = []
        for c in classes:
            result.append(self.map_class(c))
        return jsonify(result), 200

    # GET
    def get_class_by_id(self, cid):
        dao = ClassDAO()
        c = dao.get_class_by_id(cid)

        if not c:
            return jsonify(Error="Not Found"), 404
        else:
            return jsonify(self.map_class(c)), 200

    # POST
    def insert_class(self, class_json):
        dao = ClassDAO()
        cname = ccode = cdesc = term = years = cred = csyllabus = None
        if "cname" in class_json and class_json["cname"]:
            cname = class_json["cname"]
        if "ccode" in class_json and class_json["ccode"]:
            ccode = class_json["ccode"]
        if "cdesc" in class_json:
            cdesc = class_json["cdesc"]
        if "term" in class_json:
            term = class_json["term"]
        if "years" in class_json:
            years = class_json["years"]
        if "cred" in class_json:
            cred = class_json["cred"]
        if "csyllabus" in class_json:
            csyllabus = class_json["csyllabus"]

        if (cname and ccode and cdesc and term and years and cred and csyllabus and
            term in {"First Semester", "Second Semester", "According to Demand"} and
            int(cred) >= 0 and years in {"Every Year", "Even Years", "Odd Years", "According to Demand"}):

            # Validate unique class name and code concatenation
            if dao.get_class_by_name_and_code(cname, ccode):
                return jsonify(Error="Conflict"), 409

            cid = dao.insert_class(cname, ccode, cdesc, term, years, cred, csyllabus)
            temp = (cid, cname, ccode, cdesc, term, years, cred, csyllabus)
            result = self.map_class(temp)
            return jsonify(result), 201
        else:
            return jsonify(Error="Bad Request"), 400

    # DELETE
    def delete_class_by_id(self, cid):
        class_dao = ClassDAO()
        requisite_dao = RequisiteDAO()
        syllabus_dao = SyllabusDAO()
        sections_dao = SectionDAO()

        if (requisite_dao.get_requisites_by_class_id(cid) or syllabus_dao.get_syllabuses_by_class_id(cid) or
                sections_dao.get_sections_by_class_id(cid)):

            return jsonify(Error="Conflict"), 409

        temp = class_dao.delete_class_by_id(cid)
        if temp:
            return jsonify(DeleteStatus= "No Content"), 204
        else:
            return jsonify(DeleteStatus= "Not Found"), 404

    # PUT
    def update_class_by_id(self, cid, class_json):
        dao = ClassDAO()

        old_c = dao.get_class_by_id(cid)
        if old_c:
            old_c_map = self.map_class(old_c)

            if "cname" in class_json:
                new_cname = class_json["cname"]
            else:
                new_cname = old_c_map["cname"]
            if "ccode" in class_json:
                new_ccode = class_json["ccode"]
            else:
                new_ccode = old_c_map["ccode"]
            if "cdesc" in class_json:
                new_cdesc = class_json["cdesc"]
            else:
                new_cdesc = old_c_map["cdesc"]
            if "term" in class_json:
                new_term = class_json["term"]
            else:
                new_term = old_c_map["term"]
            if "years" in class_json:
                new_years = class_json["years"]
            else:
                new_years = old_c_map["years"]
            if "cred" in class_json:
                new_cred = class_json["cred"]
            else:
                new_cred = old_c_map["cred"]
            if "csyllabus" in class_json:
                new_csyllabus = class_json["csyllabus"]
            else:
                new_csyllabus = old_c_map["csyllabus"]

            if (not (new_cname and new_ccode) or
                    new_term not in {"First Semester", "Second Semester", "According to Demand"} or int(new_cred) < 0 or
                    new_years not in {"Every Year", "Even Years", "Odd Years", "According to Demand"}):
                return jsonify(Error= "Bad Request"), 400

            if dao.get_class_by_name_and_code(new_cname, new_ccode) and int(cid) != int(dao.get_class_by_name_and_code(new_cname, new_ccode)):
                return jsonify(Error= "Conflict"), 409

            status = dao.update_class_by_id(cid, new_cname, new_ccode, new_cdesc, new_term, new_years, new_cred, new_csyllabus)
            if status:
                temp = (cid, new_cname, new_ccode, new_cdesc, new_term, new_years, new_cred, new_csyllabus)
                result = self.map_class(temp)
                return jsonify(result), 200
            else:
                return jsonify(Error= "Not Found"), 404
        else:
            return jsonify(Error= "Not Found"), 404