from flask import jsonify
from dao.auth import AuthDAO

class AuthHandler:
    def map_auth_name(self, name):
        result = {}
        result["name"] = name[0]

        return result

    def get_name_from_auth(self, auth_json):
        dao = AuthDAO()
        username = password = None
        if "username" in auth_json:
            username = auth_json["username"]
        if "password" in auth_json:
            password = auth_json["password"]

        if username and password:
            name = dao.get_name_from_auth(username, password)
            if not name:
                return jsonify(Error="Not Found"), 404
            else:
                return jsonify(self.map_auth_name(name)), 200
        else:
            return jsonify(Error="Bad Request"), 400