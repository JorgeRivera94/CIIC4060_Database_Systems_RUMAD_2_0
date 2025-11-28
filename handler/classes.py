from flask import jsonify
from dao.classes import ClassDAO

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

    def get_all_classes_test(self):
        c1 = {"cid": 2,
              "cname": "CIIC",
              "ccode": "3015",
              "cdesc": "Introduction to Computer Programming I",
              "term": "First Semester, Second Semester",
              "years": "Every Year",
              "cred": 4,
              "csyllabus": "https://www.uprm.edu/cse/wp-content/uploads/sites/153/2020/03/CIIC-3015-Introduction-to-Computer-Programming-I.pdf",
              }
        c2 = {"cid": 3,
              "cname": "CIIC",
              "ccode": "3075",
              "cdesc": "Foundations of Computing",
              "term": "First Semester, Second Semester",
              "years": "Every Year",
              "cred": 3,
              "csyllabus": "https://www.uprm.edu/cse/wp-content/uploads/sites/153/2023/10/CIIC-3075-Foundations-of-Computing.pdf",
              }
        result = [c1, c2]
        return jsonify(result)

    def get_all_classes(self):
        dao = ClassDAO()
        classes = dao.get_all_classes()
        result = []
        for c in classes:
            result.append(self.map_class(c))
        return jsonify(result)