import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'twitch_bot_django.settings'
django.setup()
from bot_commands.models import *
import urllib2
import dateutil.parser
import datetime
import pytz
import json


def custom_command(case, msg):
    if case == 'create':
        command, created = custom_commands.objects.get_or_create(command=msg.split(' ')[0],
                                                                 message=msg.replace(msg.split(' ')[0]+' ',''))
        if not created:
            return "Command already exists, use 'edit' to change custom command."
        else:
            command.save()
            return "Command created."
    elif case == 'edit':
        command = custom_commands.objects.filter(command=msg.split(' ')[0])
        if len(command) == 0:
            return "Command not found, use 'create' to make a new custom command"
        else:
            command = custom_commands.objects.update(command=msg.split(' ')[0],
                                                     message=msg.replace(msg.split(' ')[0]+' ',''))
            command.save()
            return "Command updated."
    elif case == 'delete':
        command = custom_commands.objects.delete(command=msg.split(' ')[0])
        command.save()
        return "Command deleted."
    else:
        return "Command not recognize."


def get_channel_object(channel_name):
    channel_json = urllib2.urlopen("https://api.twitch.tv/kraken/channels/"+channel_name).read()
    return json.loads(channel_json)


def uptime(channel_name):
    chan_dict = get_channel_object(channel_name)
    start_time = dateutil.parser.parse(chan_dict['updated_at'])
    current_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    time_diff = current_time - start_time
    hours, remainder = divmod(time_diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return channel_name+" has been streaming for "+str(hours)+" hours and "+str(minutes)+" minutes."


def game(channel_name):
    chan_dict = get_channel_object(channel_name)
    return channel_name + " is playing " + chan_dict['game']


def welcome_subscriber(channel_name, twitch_message):
    pass

