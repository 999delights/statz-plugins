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
import math


MaxQueue = ''
CurrentQueue = ''




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
    



def check_job_mode(speed_dir, name, server, job_mode):
    def check_file(file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                for key, values in data.items():
                    character_name, server_name = key.split('/')
                    if character_name == name and server_name == server:
                        file_job_mode = values.get('jobMode', None)
                        isChecked = values.get('checked', None)
                        if isChecked:
                            if file_job_mode is None:
                                return "Not_found"
                            elif job_mode == file_job_mode:
                                return "Same"
                            elif job_mode != file_job_mode and file_job_mode != "" and job_mode != "":
                                return "Not_same"
                            else:
                                return "Not_found"
                        else:
                            return "Not_found"
        except (IOError, json.JSONDecodeError):
            print(f"aaaError reading or parsing file: {file_path}")
        return None

    for server_name in os.listdir(speed_dir):
        server_path = os.path.join(speed_dir, server_name)
        if os.path.isdir(server_path):
            for filename in os.listdir(server_path):
                file_path = os.path.join(server_path, filename)
                if os.path.isfile(file_path) and filename.endswith(".json"):
                    result = check_file(file_path)
                    if result is not None:
                        return result

    return "Not_found"  # Default return value if no matching file is found or if job mode is empty



def disconnected():
    global CurrentQueue

    CurrentQueue = ''


def get_inventory_job_mode(character_inventory):
    try:
        items = character_inventory['items']
        if len(items) > 8:
            item_at_index_8 = items[8]
            item_name = item_at_index_8.get('name', '').lower()

            if 'thief' in item_name:
                return 'Thief'
            elif 'hunter' in item_name:
                return 'Hunter'
            else:
                return 'Merchant'
        else:
            return 'Not active'  # Index 8 is out of bounds or not enough items
    except Exception as e:
        return 'Not active'  # Handle any other errors or unexpected structure

def event_loop():
    global MaxQueue
    global CurrentQueue
   
    speed_dir = r'C:\Users\andre\AppData\Local\Programs\phBot Testing\Plugins\info\tasks\speed'
    name = get_startup_data()['character']
    server = get_startup_data()['server']
    
    create_info_statz_directory() # Create the "info" directory if it doesn't exist
    create_server_directory(server)

    filename = 'Plugins/info/statz/'+ server + '/info_'  + name +'.json'
   

    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r') as file:
            try:
                info_data = json.load(file)
            except json.JSONDecodeError:
                log("aaError decoding JSON from file: " + filename)
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
    guildData = get_guild() if get_guild() is not None else {}
    union = get_guild_union() if get_guild_union() is not None else {}
    position = get_position() if get_position() is not None else {}
    
    training_area = get_training_area() if get_training_area() is not None else {}
    quests = get_quests() if get_quests() is not None else {}
    pet = get_pets() if get_pets() is not None else {}
    logs = get_log() if get_log() is not None else ""
    skills = get_skills() if get_skills() is not None else {}
    
    exp_ratio = get_character_data()['exp_ratio'] if get_character_data() is not None else 0
    job_type = get_character_data()['job_type'] if get_character_data() is not None else ''
    



   

    x = get_character_data()['x'] if get_character_data() is not None else 0.0
    y = get_character_data()['y'] if get_character_data() is not None else 0.0
    model = get_character_data()['model'] if get_character_data() is not None else 0
    hp = get_character_data()['hp'] if get_character_data() is not None else 0
    hp_max = get_character_data()['hp_max'] if get_character_data() is not None else 0
    mp = get_character_data()['mp'] if get_character_data() is not None else 0
 
    mp_max = get_character_data()['mp_max'] if get_character_data() is not None else 0
    drop_count = get_character_data()['drop_count'] if get_character_data() is not None else 0
  

    
    
    gold =  get_character_data()['gold'] if get_character_data() is not None else 0.0
    
    gold_per_loop =  get_character_data()['gold_per_loop'] if get_character_data() is not None else 0.0
    dead = get_character_data()['dead'] if get_character_data() is not None else False
    job_level = get_character_data()['job_level'] if get_character_data() is not None else 0
    job_name = get_character_data()['job_name'] if get_character_data() is not None else ''
    
    guild = get_character_data()['guild'] if get_character_data() is not None else ''
    level = get_character_data()['level'] if get_character_data() is not None else 0
    current_exp = get_character_data()['current_exp'] if get_character_data() is not None else 0.0
    max_exp = get_character_data()['max_exp'] if get_character_data() is not None else 0.0
    sp = get_character_data()['sp'] if get_character_data() is not None else 0
    job_current_exp = get_character_data()['job_current_exp'] if get_character_data() is not None else 0.0
   
    job_max_exp = get_character_data()['job_max_exp'] if get_character_data() is not None else 0.0
    zone_name = get_character_data()['zone_name'] if get_character_data() is not None else ''
    death_count = get_character_data()['death_count'] if get_character_data() is not None else 0
    manager = get_character_data()['manager'] if get_character_data() is not None else False
   
    botting = get_character_data()['botting'] if get_character_data() is not None else False
    job_type =  get_character_data()['job_type'] if get_character_data() is not None else ''
    exp_ratio =  get_character_data()['exp_ratio'] if get_character_data() is not None else 0

    exp_hour = get_character_data()['exp_hour'] if get_character_data() is not None else 0.0
    exp_hour = 0.0 if math.isnan(exp_hour) else exp_hour
    exp_minute = get_character_data()['exp_minute'] if get_character_data() is not None else 0.0
    exp_minute = 0.0 if math.isnan(exp_minute) else exp_minute
    exp_gained = get_character_data()['exp_gained'] if get_character_data() is not None else 0.0
    exp_gained = 0.0 if math.isnan(exp_gained) else exp_gained
   
    sp_minute = get_character_data()['sp_minute'] if get_character_data() is not None else 0.0
    sp_hour = get_character_data()['sp_hour'] if get_character_data() is not None else 0.0
    sp_gained = get_character_data()['sp_gained'] if get_character_data() is not None else 0.0
    rare_drop_count = get_character_data()['rare_drop_count'] if get_character_data() is not None else 0
    kill_count = get_character_data()['kill_count'] if get_character_data() is not None else 0
    job_mode = get_inventory_job_mode(inventory)
    checkJob = check_job_mode(speed_dir,name,server,job_mode)
    

    if get_character_data()['name'] != '':
        MaxQueue = ''
        
    

    if position != {}:
        CurrentQueue = ''
    character_data = get_character_data()

    queue_data = {'MaxQueue': str(MaxQueue), 'CurrentQueue':str(CurrentQueue)}

    info_data[f"{name}/{server}"] = {
        'name' : name,
        'server': server,
        'botting': botting,
        'dead': dead,
        'death_count':death_count,   
        'drops': drop_count,
        'exp': current_exp,
        'exp_gained': exp_gained,
        'exp_hour': exp_hour,
        'exp_level': max_exp,
        'exp_minute': exp_minute,
        'gold': gold,
        'gold_per_loop': gold_per_loop,
        'guild': guild,
        'hp': hp,
        'hp_max': hp_max,
        'job_exp': job_current_exp,
        'job_level': job_level,
        'job_level_exp': job_max_exp,
        'job_name': job_name,
        'level': level,
        'model': model,
        'mp' : mp,
        'mp_max': mp_max,
        'sp':sp,
        "sp_gained": sp_gained,
        "sp_hour": sp_hour,
        "sp_minute": sp_minute,
        'x':x,
        'y':y,
        'zone_name': zone_name,
        'activeS': activeS, 
        'quests': quests, 
        'queue_data': queue_data, 
        'training_area':training_area,
        'party': party, 
        'position':position, 
        'mastery' : mastery, 
        'guildData':guildData, 
        'unionData':union, 
        'inventory': inventory, 
        'storage':storage, 
        'guildStorage':guildStorage, 
        'pouch':pouch, 
        'academy':academy, 
        "monsters": monsters, 
        'job_mode': job_mode,
        'checkJob': checkJob,
        'manager': manager,
        'kill_count':kill_count,
        
        'rare_drop': rare_drop_count,

      
    
       
        
        
        
       
        
        
        
        
        "pet":pet, 
        'log': logs, 
        'skills': skills, 
      
        'exp_ratio': exp_ratio, 
        'job_type':job_type
    }   
    x_data = {}
    x_data[f"{name}/{server}"] = { 'character_data' : character_data}


    # Export the updated dictionary to the JSON file for each character in the info dir 
    with open('Plugins/info/statz/' + server + '/info_' + name +'.json', 'w') as file:     
        json.dump(info_data, file, indent=4)

       # Export the updated dictionary to the JSON file for each character in the info dir 
    with open('Plugins/info/info_' + name +'.json', 'w') as file:     
        json.dump(x_data, file, indent=4)



            
            


log('[%s] Loaded' % __name__)
