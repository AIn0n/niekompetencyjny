import json

from RoomTemplate import RoomTemplate
from genAlgorithm import Specimen


class JsonIO:
    def read(filepath: str) -> list:
        result = []
        with open(filepath, "r") as f:
            for v in json.load(f):
                room = RoomTemplate(
                    v["name"], v["minSize"][0], v["minSize"][1], v["expandable"]
                )
                for neighbour in v["neighbors"]:
                    room.addNeighbour(neighbour)
                if v.get("exit"):
                    room.exit = v["exit"]
                result.append(room)
        return result
