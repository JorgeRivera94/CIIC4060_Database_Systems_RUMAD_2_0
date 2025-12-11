from flask import jsonify
from dao.syllabuses import SyllabusDAO

class SyllabusHandler:
    def map_fragments(self, row):
        result = {}
        result["courseid"] = row[0],
        result["did"] = row[1],
        result["chunkid"] = row[2],
        result["chunk"] = row[3]

        return result

    # POST
    def get_fragments(self, json_body):
        dao = SyllabusDAO()
        embedding_text = json_body.get("embedding_text")
        if not embedding_text:
            return jsonify(Error= "Bad Request"), 400

        rows = dao.get_fragments(embedding_text)
        result = [self.map_fragments(row) for row in rows]
        return jsonify(result), 200

    # POST
    def get_fragments_by_cname_ccode(self, json_body):
        dao = SyllabusDAO()
        embedding_text = json_body.get("embedding_text")
        cname = json_body.get("cname")
        ccode = json_body.get("ccode")

        if not (embedding_text and cname and ccode):
            return jsonify(Error= "Bad Request"), 400

        rows = dao.get_fragments_by_cname_ccode(embedding_text, cname, ccode)
        result = [self.map_fragments(row) for row in rows]
        return jsonify(result), 200

    # POST
    def get_fragments_by_cdesc(self, json_body):
        dao = SyllabusDAO()
        embedding_text = json_body.get("embedding_text")
        cdesc = json_body.get("cdesc")

        if not (embedding_text and cdesc):
            return jsonify(Error= "Bad Request"), 400

        rows = dao.get_fragments_by_cdesc(embedding_text, cdesc)
        result = [self.map_fragments(row) for row in rows]
        return jsonify(result), 200