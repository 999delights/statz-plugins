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
import urllib.request
import phBotChat
import time
import threading
from symbol import star_expr



MaxQueue = ''
CurrentQueue = ''
current_datetime_str = ''

#1st function 
def create_info_directory():
    directory = 'Plugins/info'
    if not os.path.exists(directory):
        os.makedirs(directory) 


# Function to create the "info" directory if it doesn't exist
def create_info_statz_directory():
    directory = 'Plugins/info/statz'
    if not os.path.exists(directory):
        os.makedirs(directory)


# Function to create the "server" directory if it doesn't exist
def create_server_directory(serverName):
    directory = 'Plugins/info/statz/' + serverName + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)



def handle_joymax(opcode, data):
    global MaxQueue
    global CurrentQueue


    if opcode == 0x210E:
        if data[0] == 1:
            Index = 1
            if len(data) - Index >= 2:
                MaxQueue = struct.unpack_from('<H', data, Index)[0]
                log("max: " + str(MaxQueue))
                Index += 6
            if len(data) - Index >= 2:
                CurrentQueue = struct.unpack_from('<H', data, Index)[0]
                log("current: " + str(CurrentQueue))
    return True          
    






def joined_game():
    global current_datetime_str

    try:
        # Get the current date and time
        current_datetime = datetime.now()
        
        year, month, day = current_datetime.year, current_datetime.month, current_datetime.day
        hour, minute, second  = current_datetime.hour, current_datetime.minute, current_datetime.second

        # Format the current datetime as a string
        current_datetime_str = f"{day:02d}/{month:02d}/{year} {hour:02d}:{minute:02d}:{second:02d}"

        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log('joined_game ' + current_date)
    except Exception as e:
        log(f"Error in joined_game: {str(e)}")


def disconnected():
    global CurrentQueue

    CurrentQueue = ''


def event_loop():
    global MaxQueue
    global CurrentQueue
    character_name = get_startup_data()['character']
    server_name = get_startup_data()['server']

    create_info_statz_directory() # Create the "info" directory if it doesn't exist
    create_server_directory(server_name)

    filename = 'Plugins/info/statz/'+ server_name + '/info_'  + character_name +'.json'
   

    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r') as file:
            try:
                info_data = json.load(file)
            except json.JSONDecodeError:
                log("Error decoding JSON from file: " + filename)
                info_data = {}
    else:
        info_data = {}
    

    
    party = get_party() if get_party() is not None else {}
    monsters = get_monsters() if get_monsters() is not None else {}
 


    #get the mastery (2 skills)
    # Retrieve the 'highest_levels' dictionary (assuming it contains data)
    highest_levels = get_mastery() if get_mastery() is not None else {}
    
    # Find the two highest levels in 'highest_levels'
    sorted_levels = sorted(highest_levels.items(), key=lambda x: x[1]['level'], reverse=True)[:2]
    # Create a new dictionary with the two highest level keys and their data
    mastery = {key: value for key, value in sorted_levels}
   
    # Get active skills
    activeS = get_active_skills() if get_active_skills() is not None else {}
   
    pouch = get_job_pouch() if get_job_pouch() is not None else {}
    academy = get_academy() if get_academy() is not None else {}
    inventory = get_inventory() if get_inventory() is not None else {}
    storage = get_storage() if get_storage() is not None else {}
    guildStorage = get_guild_storage() if get_guild_storage() is not None else {}
    guild = get_guild() if get_guild() is not None else {}
    union = get_guild_union() if get_guild_union() is not None else {}
    position = get_position() if get_position() is not None else {}
    startup_data = get_startup_data() if get_startup_data() is not None else {}
    training_area = get_training_area() if get_training_area() is not None else {}
    quests = get_quests() if get_quests() is not None else {}
    pet = get_pets() if get_pets() is not None else {}
    logs = get_log() if get_log() is not None else ""
    skills = get_skills() if get_skills() is not None else {}
    connectedDate = current_datetime_str
    if get_character_data()['name'] != '':
        MaxQueue = ''
        
    

    if position != {}:
        CurrentQueue = ''
    

    queue_data = {'MaxQueue': str(MaxQueue), 'CurrentQueue':str(CurrentQueue)}

    info_data[f"{character_name}/{server_name}"] = {
        'party': party, 'mastery' : mastery, 'activeS': activeS, 'position':position, 'training_area':training_area,
        'quests': quests, 'client': startup_data, 'queue_data':queue_data, 'guildData':guild, 'unionData':union, 
        'inventory': inventory, 'storage':storage, 'guildStorage':guildStorage, 'pouch':pouch, 'academy':academy, "monsters": monsters, "pet":pet, 
        'log': logs, 'skills': skills, 'connectedTime': connectedDate 
    }   
    
    # Export the updated dictionary to the JSON file for each character in the info dir 
    with open('Plugins/info/statz/' + server_name + '/info_' + character_name +'.json', 'w') as file:     
        json.dump(info_data, file, indent=4)


            


log('[%s] Loaded' % __name__)
