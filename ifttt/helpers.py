import json, time
from django.conf import settings

class IfThisThenThatHelpers():

    def is_json(myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError:
            return False
        else:
            return True

    def convert_string_time(self, str):
        ctime = time.strptime(str, settings.DATE_FORMAT )
        return ctime

    #takes time strings, not objects
    def calculate_hours_diff(self, entered_time, exited_time):
        entered_obj = convert_string_time(entered_time)
        exited_obj = convert_string_time(exited_time)
        return abs((exited - entered).hours)
