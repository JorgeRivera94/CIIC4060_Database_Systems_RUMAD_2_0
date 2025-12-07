from flask import Flask, request, jsonify
from flask_cors import CORS
from handler.classes import ClassHandler
from handler.meetings import MeetingHandler
from handler.requisites import RequisiteHandler
from handler.rooms import RoomHandler
from handler.sections import SectionHandler
from handler.statistics import StatisticHandler
import os

app = Flask(__name__)
CORS(app)

@app.route('/Fulcrum/api')
def greeting():
    return "Fulcrum Project Base"

@app.route('/Fulcrum/api/classes', methods=["GET", "POST"])
def get_class():
    if request.method == "GET":
        return ClassHandler().get_all_classes()
    elif request.method == "POST":
        return ClassHandler().insert_class(request.json)
    else:
        return jsonify("Method Not Supported"), 405

@app.route('/Fulcrum/api/classes/<int:cid>', methods=["GET", "PUT", "DELETE"])
def get_class_by_id(cid):
    if request.method == "GET":
        return ClassHandler().get_class_by_id(cid)
    elif request.method == "PUT":
        return ClassHandler().update_class_by_id(cid, request.json)
    elif request.method == "DELETE":
        return ClassHandler().delete_class_by_id(cid)
    else:
        return jsonify("Method Not Supported"), 405

@app.route('/Fulcrum/api/room', methods=["GET", "POST"])
def get_room():
    if request.method == "GET":
        return RoomHandler().get_all_rooms()
    elif request.method == "POST":
        return RoomHandler().insert_room(request.json)
    else:
        return jsonify("Method Not Supported"), 405

@app.route('/Fulcrum/api/room/<int:rid>', methods=["GET", "PUT", "DELETE"])
def get_room_by_id(rid):
    if request.method == "GET":
        return RoomHandler().get_room_by_id(rid)
    elif request.method == "PUT":
        return RoomHandler().update_room_by_id(rid, request.json)
    elif request.method == "DELETE":
        return RoomHandler().delete_room_by_id(rid)
    else:
        return jsonify("Method Not Supported"), 405

@app.route("/Fulcrum/api/meeting", methods=["GET", "POST"])
def get_meeting():
    if request.method == "GET":
        return MeetingHandler().get_all_meetings()
    elif request.method == "POST":
        return MeetingHandler().insert_meeting(request.json)
    else:
        return jsonify("Method Not Supported"), 405

@app.route("/Fulcrum/api/meeting/<int:mid>", methods=["GET", "PUT", "DELETE"])
def get_meeting_by_id(mid):
    if request.method == "GET":
        return MeetingHandler().get_meeting_by_id(mid)
    elif request.method == "PUT":
        return MeetingHandler().update_meeting_by_id(mid, request.json)
    elif request.method == "DELETE":
        return MeetingHandler().delete_meeting_by_id(mid)
    else:
        return jsonify("Method Not Supported"), 405

@app.route("/Fulcrum/api/section", methods=["GET", "POST"])
def get_section():
    if request.method == "GET":
        return SectionHandler().get_all_sections()
    elif request.method == "POST":
        return SectionHandler().insert_section(request.json)
    else:
        return jsonify("Method Not Supported"), 405

@app.route("/Fulcrum/api/section/<int:sid>", methods=["GET", "PUT", "DELETE"])
def get_section_by_id(sid):
    if request.method == "GET":
        return SectionHandler().get_section_by_id(sid)
    elif request.method == "PUT":
        return SectionHandler().update_section_by_id(sid, request.json)
    elif request.method == "DELETE":
        return SectionHandler().delete_section_by_id(sid)
    else:
        return jsonify("Method Not Supported"), 405

@app.route("/Fulcrum/api/requisite", methods=["GET", "POST"])
def get_requisite():
    if request.method == "GET":
        return RequisiteHandler().get_all_requisites()
    elif request.method == "POST":
        return RequisiteHandler().insert_requisite(request.json)
    else:
        return jsonify("Method Not Supported"), 405

@app.route("/Fulcrum/api/requisite/<int:classid>/<int:reqid>", methods=["GET", "DELETE"])
def get_requisite_by_id(classid, reqid):
    if request.method == "GET":
        return RequisiteHandler().get_requisite_by_id(classid, reqid)
    elif request.method == "DELETE":
        return RequisiteHandler().delete_requisite_by_id(classid, reqid)
    else:
        return jsonify("Method Not Supported"), 405

@app.route("/Fulcrum/api/stats/sections-by-day", methods=["GET"])
def get_sections_by_day_of_week():
    if request.method == "GET":
        return StatisticHandler().get_sections_by_day_of_week(request.json)
    else:
        return jsonify("Method Not Supported"), 405

@app.route("/Fulcrum/api/stats/top-classes-by-avg-duration/", methods=["GET"])
def get_top_classes_by_avg_duration():
    if request.method == "GET":
        return StatisticHandler().get_top_classes_by_avg_duration(request.json)
    else:
        return jsonify("Method Not Supported"), 405

@app.route("/Fulcrum/api/stats/top-rooms-by-utilization", methods=["GET"])
def get_top_rooms_by_utilization():
    if request.method == "GET":
        return StatisticHandler().get_top_rooms_by_utilization(request.json)
    else:
        return jsonify("Method Not Supported"), 405

@app.route("/Fulcrum/api/stats/multi-room-classes", methods=["GET"])
def get_multi_room_classes():
    if request.method == "GET":
        return StatisticHandler().get_multi_room_classes(request.json)
    else:
        return jsonify("Method Not Supported"), 405

@app.route("/Fulcrum/api/stats/top-departments-by-sections", methods=["GET"])
def get_top_departments_by_sections():
    if request.method == "GET":
        return StatisticHandler().get_top_departments_by_sections(request.json)
    else:
        return jsonify("Method Not Supported"), 405

@app.route("/Fulcrum/api/stats/classes-without-prereqs", methods=["GET"])
def get_classes_without_prereqs():
    if request.method == "GET":
        return StatisticHandler().get_classes_without_prereqs()
    else:
        return jsonify("Method Not Supported"), 405

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)