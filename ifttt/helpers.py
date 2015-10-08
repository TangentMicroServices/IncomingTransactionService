import json, requests
from django.conf import settings
from datetime import datetime
from microclient.clients import HoursService, UserService, ProjectService

def convert_string_time(str):
    ctime = datetime.strptime(str, settings.DATE_FORMAT )
    return ctime

def quick_validate(required_fields, payload):
    for field in required_fields:
        assert field in payload

def hipchat_speak(message, from_name="Mr Robot"):
    '''
    Utility to make it easy to post to hipchat 
    Includes this app's context
    '''

    '''
    url = "https://api.hipchat.com/v2/room/{}/notification?auth_token={}" . format (room, token)
    return requests.post(url, {"message":message})
    '''
    token = settings.HIPCHAT_AUTH_TOKEN
    room = settings.HIPCHAT_ROOM_ID
    
    url ='https://api.hipchat.com/v1/rooms/message?format=json&auth_token={}' . format (token)
    data = {
        "room_id": room,
        "from": from_name,
        "message": message,
        "message_format": "text"
    }
    return requests.post(url, data)
    
def get_current_user(token, user_id):
    service = UserService(token=token, tld=settings.MICROSERVICE_TLD)
    return service.get(resource='user', resource_id=user_id)

def get_project(token, project_id):
    service = ProjectService(token=token, tld=settings.MICROSERVICE_TLD)
    return service.get(resource='project', resource_id=project_id)

def get_hipchat_message(user, project, entered_or_exited):

    assert entered_or_exited in ['entered', 'exited'], \
    "entered_or_exited must be either 'entered', or 'exited"

    user_name = user.get("first_name", None)
    project_name = project.get("title", None)

    message_templates = {
        "entered": "{} has arrived at {}",
        "exited": "{} has left {}"
    }

    return message_templates.get(entered_or_exited).format(user_name, project_name)



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
        token = payload["auth_token"]
        service = HoursService(token=token, tld=settings.MICROSERVICE_TLD)
        # get date
        # datetime.datetime.now() won't work because already imported datetime from datetime
        i = datetime.now()
        data = {
            "user": payload["user"],
            "project_id":payload["project_id"],
            "project_task_id":payload["project_task_id"],
            "day": "{}-{}-{}" .format (i.year, i.month, i.day),
            "hours": hours,
            "comments": payload.get("comment", "default comment")
        }

        return service.create(resource="entry", data=data)

    @staticmethod 
    def post_to_hipchat(payload):
        """
        Given an IFTTT payload, correctly post messages to HipChat
        """
        
        required_fields = ['user', 'project_id', 'entered_or_exited', 'auth_token']
        quick_validate(required_fields, payload)        

        token = payload.get('auth_token')
        user_id = payload.get('user')
        project_id = payload.get('project_id')
        entered_or_exited = payload.get('entered_or_exited')

        user = get_current_user(token, user_id).json() 
        project = get_project(token, project_id).json()

        message = get_hipchat_message(user, project, entered_or_exited)

        hipchat_speak(message)

    @staticmethod
    def get_hours(enter_payload, exit_payload):
        """
        pass in the two payloads, get the dates, return the hours count
        """
        entered_date = enter_payload["time"]
        exited_date = exit_payload["time"]

        return IfThisThenThatHelpers.calculate_hours_diff(entered_date, exited_date)
        

    #takes time strings, not objects
    @staticmethod
    def calculate_hours_diff(entered_time, exited_time):

        entered = convert_string_time(entered_time)
        exited = convert_string_time(exited_time)
        delta = (exited - entered)
        seconds = abs(delta.days * 86400) + delta.seconds
        hours = IfThisThenThatHelpers.round_to(seconds/3600.0, 0.5)

        #import pdb;pdb.set_trace()

        if exited < entered:
            hours=hours*-1

        return hours

    @staticmethod
    def round_to(n, precision):
        correction = 0.5 if n >= 0 else -0.5
        return int( n/precision+correction ) * precision
