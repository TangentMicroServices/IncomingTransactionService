import json
from django.conf import settings
from datetime import datetime
from microclient.clients import HoursService

def convert_string_time(str):
    ctime = datetime.strptime(str, settings.DATE_FORMAT )
    return ctime


class IfThisThenThatHelpers:

    @staticmethod
    def is_json(myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError:
            return False
        else:
            return True

    @staticmethod
    def make_hours_post(payload, hours):
        # initialise the hours service
        service = HoursService(token=payload["auth_token"], tld=settings.MICROSERVICE_TLD)
        # get date
        # datetime.datetime.now() won't work because already imported datetime from datetime
        i = datetime.now()
        data = {
            "user": payload["user"],
            "project_id":payload["project_id"],
            "project_task_id":payload["project_task_id"],
            "day": "{}-{}-{}" .format (i.year, i.month, i.day),
            "hours": hours,
            "comments": "testing"
        }
        
        return service.create(resource="entry", data=data)
        

    @staticmethod
    def get_hours(enter_payload, exit_payload):
        """
        pass in the two payloads, get the dates, return the hours count
        """
        entered_date = enter_payload["time"]
        exited_date = exit_payload["time"]

        hours = IfThisThenThatHelpers.calculate_hours_diff(entered_date, exited_date)
        if hours in range(1, 24):
            return hours
        else:
            raise Exception("Hours out of Range")


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
