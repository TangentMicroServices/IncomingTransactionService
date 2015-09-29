import json

class IfThisThenThatHelpers():

    def is_json(myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError:
            return False
        else:
            return True
