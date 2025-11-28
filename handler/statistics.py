from flask import jsonify
from dao.statistics import StatisticDAO

class StatisticHandler:
    def map_top_classes_by_avg_duration(self, statistic):
        result = {}
        result["cid"] = statistic[0]
        result["fullcode"] = statistic[1]
        result["avg_minutes"] = statistic[2]

        return result

    def map_classes_without_prereqs(self, statistic):
        result = {}
        result["cid"] = statistic[0]
        result["fullcode"] = statistic[1]

        return result

    def get_top_classes_by_avg_duration(self, statistic_json):
        dao = StatisticDAO()
        year = semester = limit = None
        if "year" in statistic_json:
            year = statistic_json["year"]
        if "semester" in statistic_json:
            semester = statistic_json["semester"]
        if "limit" in statistic_json:
            limit = statistic_json["limit"]
            if not limit:
                limit = 1
        else:
            limit = 1

        if year and semester and limit:
            if not (year.isnumeric() and len(year) == 4 and
                    semester in {"Fall", "Spring", "V1", "V2"} and
                    1 <= limit <= 10):
                return jsonify(Error="Bad Request"), 400

            if dao.define_get_duration():
                durations = dao.get_top_classes_by_avg_duration(year, semester, limit)
                result = []
                for duration in durations:
                    result.append(self.map_top_classes_by_avg_duration(duration))
                return jsonify(result), 200

            else:
                return jsonify(Error="Internal Server Error"), 500
        else:
            return jsonify(Error="Bad Request"), 400

    def get_classes_without_prereqs(self):
        dao = StatisticDAO()
        classes = dao.get_classes_without_prereqs()
        result = []
        for c in classes:
            result.append(self.map_classes_without_prereqs(c))
        return jsonify(result), 200