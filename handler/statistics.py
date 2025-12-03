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

    def map_sections_by_day_of_week(self, statistic):
        result = {}
        result["sid"] = statistic[0]
        result["cdays"] = statistic[1]

        return result

    def map_top_rooms_by_utilization(self, statistic):
        result = {}
        result["rid"] = statistic[0]
        result["building"] = statistic[1]
        result["room_number"] = statistic[2]
        result["utilization"] = statistic[3]

        return result

    def get_sections_by_day_of_week(self, statistic_json):
        dao = StatisticDAO()
        year = semester = None
        if "year" in statistic_json:
            year = statistic_json["year"]
        if "semester" in statistic_json:
            semester = statistic_json["semester"]

        if (year and semester and semester in {"Fall", "Spring", "V1", "V2"}
                and len(str(year)) == 4 and str(year).isnumeric()):

            days_freq = {"L":0, "M":0, "W":0, "J":0, "V":0, "S":0, "D":0}
            temp = dao.get_sections_by_day_of_week(year, semester)
            sections_and_days = []
            for row in temp:
                sections_and_days.append(self.map_sections_by_day_of_week(row))
            for sid in sections_and_days:
                if "L" in sid["cdays"]:
                    days_freq["L"] += 1
                if "M" in sid["cdays"]:
                    days_freq["M"] += 1
                if "W" in sid["cdays"]:
                    days_freq["W"] += 1
                if "J" in sid["cdays"]:
                    days_freq["J"] += 1
                if "V" in sid["cdays"]:
                    days_freq["V"] += 1
                if "S" in sid["cdays"]:
                    days_freq["S"] += 1
                if "D" in sid["cdays"]:
                    days_freq["D"] += 1

            result = []
            for day in ("L", "M", "W", "J", "V", "S", "D"):
                result.append({"day": day, "sections": days_freq[day]})

            return jsonify(result), 200

        else:
            return jsonify(Error= "Bad Request"), 400

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

    def get_top_rooms_by_utilization(self, statistic_json):
        dao = StatisticDAO()
        year = semester = limit = None
        if "year" in statistic_json:
            year = statistic_json["year"]
        if "semester" in statistic_json:
            semester = statistic_json["semester"]
        if "limit" in statistic_json:
            limit = statistic_json["limit"]
            if not limit:
                limit = 5
        else:
            limit = 5
        if (year and semester and limit and str(year).isnumeric() and len(str(year)) == 4
                and semester in {"Fall", "Spring", "V1", "V2"} and 1 <= int(limit) <= 10):

            top_rooms = dao.get_top_rooms_by_utilization(year, semester, limit)
            result = []
            for room in top_rooms:
                result.append(self.map_top_rooms_by_utilization(room))
            return jsonify(result), 200
        else:
            return jsonify(Error="Bad Request"), 400

    def get_classes_without_prereqs(self):
        dao = StatisticDAO()
        classes = dao.get_classes_without_prereqs()
        result = []
        for c in classes:
            result.append(self.map_classes_without_prereqs(c))
        return jsonify(result), 200