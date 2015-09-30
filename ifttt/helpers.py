import json
from django.conf import settings
from datetime import datetime

def convert_string_time(str):
    ctime = datetime.strptime(str, settings.DATE_FORMAT )
    return ctime


class IfThisThenThatHelpers:

    def is_json(myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError:
            return False
        else:
            return True

    #takes time strings, not objects
    @staticmethod
    def calculate_hours_diff(entered_time, exited_time):

        entered = convert_string_time(entered_time)
        exited = convert_string_time(exited_time)
        delta = (exited - entered)
        seconds = abs(delta.days * 86400) + delta.seconds
        #import pdb;pdb.set_trace()
        hours = round(seconds/3600)
        
        if exited < entered:
            hours=hours*-1

        return hours
