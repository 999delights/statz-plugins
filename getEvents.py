from calendar import c
from http import server
from math import e
from queue import Empty
from re import L, U
import struct
from turtle import pos
from phBot import *
import json
import os
from datetime import datetime
from symbol import star_expr


def event_name(event_type):
    if event_type == 0:
        return "EVENT_UNIQUE_SPAWN"
    elif event_type == 1:
        return "EVENT_HUNTER_SPAWN"
    elif event_type == 2:
        return "EVENT_THIEF_SPAWN"
    elif event_type == 3:
        return "EVENT_TRANSPORT_DIED"
    elif event_type == 4:
        return "EVENT_PLAYER_ATTACKING"
    elif event_type == 5:
        return "EVENT_RARE_DROP"
    elif event_type == 6:
        return "EVENT_ITEM_DROP"
    elif event_type == 7:
        return "EVENT_DIED"
    elif event_type == 8:
        return "EVENT_ALCHEMY_FINISHED"
    elif event_type == 9:
        return "EVENT_GM_SPAWNED"
    elif event_type == 10:
        return "EVENT_LEVEL_UP"
    else:
        return "UNKNOWN_EVENT"



#1st function 
def create_info_directory():
    directory = 'Plugins/info'
    if not os.path.exists(directory):
        os.makedirs(directory) 

# Function to create the "info" directory if it doesn't exist
def create_info_events_directory():
    directory = 'Plugins/info/events'
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to create the "server" directory if it doesn't exist
def create_server_directory(serverName):
    directory = 'Plugins/info/events/' + serverName + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to create the "character" directory if it doesn't exist
def create_character_directory(serverName, character_name):
    directory = 'Plugins/info/events/' + serverName + '/' + character_name + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)



def get_current_datetime_str():
    # Get the current datetime
    current_datetime = datetime.now()
    
    # Extract year, month, day, hour, minute, and second
    year, month, day = current_datetime.year, current_datetime.month, current_datetime.day
    hour, minute, second = current_datetime.hour, current_datetime.minute, current_datetime.second
    
    # Format the current datetime as a string
    current_datetime_str = f"{day:02d}/{month:02d}/{year} {hour:02d}:{minute:02d}:{second:02d}"
    
    return current_datetime_str

def ritual():
    character_name = get_startup_data()['character']
    server_name = get_startup_data()['server']
    create_info_events_directory()  # Create the "info" directory if it doesn't exist
    create_server_directory(server_name)
    create_character_directory(server_name, character_name)
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
   
    filename = 'Plugins/info/events/' + server_name + '/' + character_name + '/' + current_date +'.json'

    return filename

def joined_game():
    character_name = get_startup_data()['character']
    server_name = get_startup_data()['server']
    event_name = 'EVENT_CONNECTED'
    
    date = get_current_datetime_str()
    filename = ritual()
    event_data = {}
    # Create a dictionary with event name as key and data as value
    event_data[f"{character_name}/{server_name}"] = {'event_name': event_name, 'date': date, 'data': '' }  
 
    # Write the dictionary to a JSON file
    with open(filename, 'w') as file:
        json.dump(event_data, file, indent=4)


def disconnected():
    character_name = get_startup_data()['character']
    server_name = get_startup_data()['server']
    event_name = 'EVENT_DISCONNECTED'
    date = get_current_datetime_str()
    filename = ritual()

    event_data = {}
    # Create a dictionary with event name as key and data as value
    
    event_data[f"{character_name}/{server_name}"] = {'event_name': event_name, 'date': date, 'data': ''}  
    # Write the dictionary to a JSON file
    with open(filename, 'w') as file:
        json.dump(event_data, file, indent=4)



def finished():
    character_name = get_startup_data()['character']
    server_name = get_startup_data()['server']
    event_name = 'EVENT_DISCONNECTED'
    date = get_current_datetime_str()
    filename = ritual()

    event_data = {}
    # Create a dictionary with event name as key and data as value
    
    event_data[f"{character_name}/{server_name}"] = {'event_name': event_name, 'date': date, 'data': ''}  
    # Write the dictionary to a JSON file
    with open(filename, 'w') as file:
        json.dump(event_data, file, indent=4)






def handle_event(t, data):
    character_name = get_startup_data()['character']
    server_name = get_startup_data()['server']
    event_name = event_name(t)
    
    data = data
    date = get_current_datetime_str()
    filename = ritual()
    event = {'event_name': event_name, 'date': date, 'data': data}
    event_data = {}
    event_data[f"{character_name}/{server_name}"] = {'events': event}  # Create a dictionary with char name as key and event as value
    
    # Write the dictionary to a JSON file
    with open(filename, 'w') as file:
        json.dump(event_data, file, indent=4)


log('[%s] Loaded' % __name__)
