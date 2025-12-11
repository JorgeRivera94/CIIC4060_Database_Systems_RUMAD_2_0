import os
import requests
from typing import List, Dict, Any

HEROKU_API_BASE = "http://db-ciic4060-team-fulcrum-3d540ddad512.herokuapp.com/Fulcrum/api"

class RemoteSyllabusClient:
    def __init__(self, base_url: str = HEROKU_API_BASE):
        self.base_url = base_url

    def _post(self, path: str, payload: Dict[str, Any]) -> Any:
        url = f"{self.base_url}{path}"
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def get_fragments(self, embedding_text: str) -> List[Dict[str, Any]]:
        return self._post("/syllabus/fragments", {"embedding_text": embedding_text})

    def get_fragments_by_cname_ccode(
        self, embedding_text: str, cname: str, ccode: str
    ) -> List[Dict[str, Any]]:
        return self._post(
            "/syllabus/fragments-by-code",
            {"embedding_text": embedding_text, "cname": cname, "ccode": ccode},
        )

    def get_fragments_by_cdesc(
        self, embedding_text: str, cdesc: str
    ) -> List[Dict[str, Any]]:
        return self._post(
            "/syllabus/fragments-by-cdesc",
            {"embedding_text": embedding_text, "cdesc": cdesc},
        )


class RemoteClassClient:
    def __init__(self, base_url: str = HEROKU_API_BASE):
        self.base_url = base_url

    def get_all_cdesc(self) -> list[str]:
        url = f"{self.base_url}/classes/cdesc"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # Expect data to be a list of strings
        return [str(x) for x in data]