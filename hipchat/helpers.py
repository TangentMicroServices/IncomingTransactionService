def parse_hipchat_message(message):
    """
    Takes the incoming slash command and translates it to an Entry
    """
    slash_command_split = str.split(message, ' ')
    comments = " ".join(slash_command_split[3: len(slash_command_split)])
    entry = {
        'project_id': str.split(slash_command_split[1], ":")[0],
        'project_task_id': str.split(slash_command_split[1], ":")[1],
        'hours': slash_command_split[2],
        'comments': comments,
    }
    return entry

def get_user(email):
    """
    Fetch a user given their e-mail address
    """
    pass

def get_hipchat_user(self, hipchat_user_id):
    pass

