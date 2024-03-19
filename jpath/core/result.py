import json


class Result:
    def __init__(self, json_data):
        self.json_data = json_data

    def __str__(self):
        # pretty print json dump
        return json.dumps(self.json_data, indent=2)

    def __repr__(self):
        return self.__str__()
