from calendar import c
from math import e
from queue import Empty
from re import U
import struct
from turtle import pos
from phBot import *
import json
import os
from datetime import datetime
import urllib.request
import phBotChat

import time



speed_dir = r'C:\Users\andre\AppData\Local\Programs\phBot Testing\Plugins\info\tasks\speed'





# Initialize a global variable to keep track of the last call time outside of your function
last_cast_time = 0

def event_loop():
    global last_cast_time
sss
    # Get the current time
    current_time = time.time()

    # Check if at least 5 seconds have passed since the last call
    if current_time - last_cast_time >= 5:
        if get_character_data()['name'] != "":
            character_name = get_startup_data()['character']
            server_name = get_startup_data()['server']
            hp = get_character_data()['hp'] if get_character_data() is not None else 0
            party = get_party() if get_party() is not None else {}   
            training_area = get_training_area() if get_training_area() is not None else {}
            position = get_position() if get_position() is not None else {}
            job_name = get_character_data()['job_name'] if get_character_data() is not None else ''
            
            # Call cast_speed only if 5 seconds have passed
            cast_speed(character_name, server_name, position, training_area, party, hp)

            # Update the last_cast_time to the current time after calling cast_speed
            last_cast_time = current_time
       



def cast_speed( name,server,position,training_area,party,hp):

    
    
    # Check if the directory exists
    if not os.path.exists(speed_dir):
        log("The directory" + speed_dir +" does not exist!")
        return
    
    for server_name in os.listdir(speed_dir):
        server_path = os.path.join(speed_dir, server_name)
        if os.path.isdir(server_path):
            # Iterate through each character JSON file in the server directory
            # Loop through each file in the directory
            for filename in os.listdir(server_path):
                # Construct full file path
                file_path = os.path.join(server_path, filename)
                
                # Check if it's a file and has a .json extension
                if os.path.isfile(file_path) and filename.endswith(".json"):

                    # Load the JSON content
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        for key, values in data.items():
                            character_name, server_name = key.split('/')
                            if(character_name == name and server == server_name):
                                checked = values.get('checked', False)
                                item_list = values.get('list', [])
                                charName_list = []
                                jobName_list = []

                                for item in item_list:
                                    charName, jobName = item.split('/', 1)  # Split each string by the first '/' encountered
                                    charName_list.append(charName)
                                    jobName_list.append(jobName)

                                is_bard = values.get('isBard', False)
                                jobMode = values.get('jobMode', '')
                            
                                if checked: # if speed is needed
                                    
                                    if not is_bard:  # if not bard
                                        
                                        is_not_found = search_speed()  
                                        
                                        if is_not_found:  # if any speed not found  -
                                            
                                            inParty = party
                                            
                                            if inParty is not Empty:    # if in a party
                                                
                                                
                                                    # First check the priority player
                                                for player_data in party.values():
                                                    player_name = player_data['name']
                                                    if jobMode != "Not active":

                                                        if player_name in jobName_list:
                                                            x = player_data['x']
                                                            y = player_data['y']
                                                            region = player_data['region']
                                                            pos = {'x': x, 'y': y, 'region': region}
                                                            hp_percent = player_data['hp_percent']
                                                            playerInTrainingArea = isInTrainingArea(pos, training_area)
                                                            
                                                            if playerInTrainingArea and int(hp_percent) != 0 and isInTrainingArea(position, training_area): # if both in training area
                                                                if int(hp) != 0:
                                                                    return phBotChat.Party("speeddeeps")
                                                                # return from the function as soon as priority player is found in the area
                                                    elif jobMode == "Not active":
                                                        if player_name in charName_list:
                                                            x = player_data['x']
                                                            y = player_data['y']
                                                            region = player_data['region']
                                                            pos = {'x': x, 'y': y, 'region': region}
                                                            hp_percent = player_data['hp_percent']
                                                            playerInTrainingArea = isInTrainingArea(pos, training_area)
                                                            
                                                            if playerInTrainingArea and int(hp_percent) and isInTrainingArea(position, training_area): # if both in training area
                                                                if int(hp) != 0:
                                                                    return phBotChat.Party("speeddeeps")
                                                                    # return from the function as soon as priority player is found in the area
                                                        
                                    

#Message type
def messageType(type):
    if type == 1:
        return "general"
    elif type == 2:
        return "private"
    elif type == 3:
        return "gm"
    elif type == 4:
        return "party"
    elif type == 5:
        return "guild"
    elif type == 6:
        return "global"
    elif type == 7:
        return "notice"
    elif type == 9:
        return "stall"
    elif type == 11:
        return "union"
    elif type == 16:
        return "academy"
    else:
        return "all"                                

def determine_march(skills):
    # Default march to an empty string
    march = ''

    # Assuming 'skills' is a dictionary with string keys and dictionaries as values, each representing a skill.
    found_skill = next((skill for skill in skills.values() if skill['name'] == 'Swing March'), None)

    if found_skill:
        march = 'Swing March'
    else:
        # If Swing March is not found, default to Moving March
        march = 'Moving March'

    # If not a bard, it's assumed that logic to not call this function or handle its result accordingly is handled elsewhere.
    return march


def GetSkillID(name):
    skills = get_skills()
    for ID, skill in skills.items():
        if skill['name'] == name:
            return ID

def CastSkill(name):
    
    ID = GetSkillID(name)
    p = b'\x01\x04'
    p += struct.pack('<I', ID)
    p += b'\x00'
    log("a")
    inject_joymax(0x7074,p, False)
    log("Plugin: Casting [%s]" %name)





def checkMyTrainingAreaPlusHp(hp,position,training_area,march):
    inTrainingArea = isInTrainingArea(position, training_area) 
    if inTrainingArea:
        if int(hp) != 0:
            return start_script("recast,Swing March")
    
          
def allNotInTrainingAreaOrZeroHP(inParty, jobName_list, training_area):
    allNotInTrainingAreaOrZeroHP = True

    for player_name in jobName_list:
        # Only process players mentioned in jobName_list
        if player_name in inParty:
            player_data = inParty[player_name]

            x = player_data['x']
            y = player_data['y']
            region = player_data['region']
            hp_percent = player_data['hp_percent']
            pos = {'x': x, 'y': y, 'region': region}

            playerInTrainingArea = isInTrainingArea(pos, training_area)

            # If any player is in the training area and has HP > 0, set the flag to False
            if playerInTrainingArea and int(hp_percent) > 0:
                allNotInTrainingAreaOrZeroHP = False
                break  # No need to check further, at least one player doesn't meet the criteria

    return allNotInTrainingAreaOrZeroHP


def handle_chat(t, player, msg):  
    message = str(msg)
    message = urllib.parse.quote(message)
    type = str(messageType(t))
    sender = str(player)
    if type == "party":
        if message == "speeddeeps":



            name = get_startup_data()['character']
            server = get_startup_data()['server']
            hp = get_character_data()['hp'] if get_character_data() is not None else 0
            party = get_party() if get_party() is not None else {}   
            training_area = get_training_area() if get_training_area() is not None else {}
            position = get_position() if get_position() is not None else {}
            playerInTrainingArea = False  # Initialize this to False
            
          
            skills = get_skills() if get_skills() is not None else {}
            march = determine_march(skills)

            # Loop through each file in the directory
            for server_name in os.listdir(speed_dir):
                server_path = os.path.join(speed_dir, server_name)
                if os.path.isdir(server_path):
                    for filename in os.listdir(server_path):
                        # Construct full file path
                        file_path = os.path.join(server_path, filename)
                    
                       
                        # Check if it's a file and has a .json extension
                        if os.path.isfile(file_path) and filename.endswith(".json"):
                               
                            # Load the JSON content
                            with open(file_path, 'r') as file:
                                data = json.load(file)
                                for key, values in data.items():
                                    character_name, server_name = key.split('/')
                                    if(character_name == name and server_name == server):
                                        checked = values.get('checked', False)
                                        item_list = values.get('list', [])  # Assuming 'values' is already defined
                                        charName_list = []
                                        jobName_list = []

                                        for item in item_list:
                                            charName, jobName = item.split('/', 1)  # Split each string by the first '/' encountered
                                            charName_list.append(charName)
                                            jobName_list.append(jobName)

                                        jobMode = values.get('jobMode', '')
                                        is_bard = values.get('isBard', False)
                                        main = values.get('main', "")
                                        if checked:     # if cast speed is checked 
                                            if is_bard == True: # if is bard
                                                inParty = party
                                                if inParty is not Empty: 
                                                    if main == "Main":   
                                                        checkMyTrainingAreaPlusHp(hp,position,training_area,march)
                                                    else:
                                                        if jobMode != "Not active":
                                                            if jobName_list is not Empty:          # if other players are prior
                                                                
                                                                if allNotInTrainingAreaOrZeroHP(inParty,jobName_list,training_area):
                                                                    checkMyTrainingAreaPlusHp(hp,position,training_area,march)        
                                                            else:
                                                                checkMyTrainingAreaPlusHp(hp,position,training_area,march)
                                                                   
                                                        elif jobName == "Not active":
                                                                
                                                            if allNotInTrainingAreaOrZeroHP(inParty,jobName_list,training_area):
                                                                checkMyTrainingAreaPlusHp(hp,position,training_area,march)        
                                                            else:
                                                                checkMyTrainingAreaPlusHp(hp,position,training_area,march)
                                                                                    
                                                                                 

                                                                    
                                                                
                                                            
                                                                

                                                    

                                
                    
            





def search_speed():
    skill_data = get_active_skills()
    if skill_data is None:
        log("Failed to retrieve skill data.")
        return False
    
    # List of skills to search for
    skills_to_check = [
        "Beginner scroll of movement",
        "Drug of wind",
        "Drug of typoon",
        "Swing March",
        "Moving March"
    ]

    # Assuming skill_data is a dictionary with keys being skill IDs and values being skill information
    for skill_id, skill_info in skill_data.items():
        if skill_info['name'] in skills_to_check:
            return False

    return True



def isInTrainingArea(characterPosition, trainingArea):
    if not characterPosition or not trainingArea:
        return False

    radius = trainingArea['radius']

    if characterPosition['region'] == trainingArea['region']:
        if characterPosition['region'] >= 0:
            # For non-dungeon
            charAX = get_aX_ND(characterPosition['x'])
            charBY = get_bY_ND(characterPosition['y'])
            charA = get_A_ND(characterPosition['x'])
            charB = get_B_ND(characterPosition['y'])

            trainingAX = get_aX_ND(trainingArea['x'])
            trainingBY = get_bY_ND(trainingArea['y'])
            trainingA = get_A_ND(trainingArea['x'])
            trainingB = get_B_ND(trainingArea['y'])

            return (charA == trainingA and
                    charB == trainingB and
                    abs(charAX - trainingAX) <= radius and
                    abs(charBY - trainingBY) <= radius)

        else:
            # For dungeon
            charX2 = getNew_X(characterPosition['x'], characterPosition['region'])
            charY2 = getNew_Y(characterPosition['y'], characterPosition['region'])
            charAX = get_aX_D(charX2)
            charBY = get_bY_D(charY2)
            charA = get_A_D(charX2)
            charB = get_B_D(charY2)

            trainingX2 = getNew_X(trainingArea['x'], trainingArea['region'])
            trainingY2 = getNew_Y(trainingArea['y'], trainingArea['region'])
            trainingAX = get_aX_D(trainingX2)
            trainingBY = get_bY_D(trainingY2)
            trainingA = get_A_D(trainingX2)
            trainingB = get_B_D(trainingY2)

            return (charA == trainingA and
                    charB == trainingB and
                    abs(charAX - trainingAX) <= radius/200 and
                    abs(charBY - trainingBY) <= radius/200)
    
    return False

# GET A NON DUNGEON
def get_A_ND(x):
    return int(x / 192 + 135)

# GET B NON DUNGEON
def get_B_ND(y):
    return int(y / 192 + 92)

# GET A DUNGEON
def get_A_D(x):
    return (128 * 192 + x / 10) // 192

# GET B DUNGEON
def get_B_D(y):
    return (128 * 192 + y / 10) // 192

# GET aX NON DUNGEON
def get_aX_ND(x):
    return (x / 192 + 135) - (x / 192 + 135) // 1 - 0.015

# GET bY NON DUNGEON
def get_bY_ND(y):
    return (y / 192 + 92) - (y / 192 + 92) // 1 - 0.04

# GET aX DUNGEON
def get_aX_D(x):
    value = (128 * 192 + x / 10) / 192
    return value - value // 1 - 0.015

# GET bY DUNGEON
def get_bY_D(y):
    value = (128 * 192 + y / 10) / 192
    return value - value // 1 - 0.04

# GET newX
def getNew_X(x, region):
    return 10 * (x - ((region & 255) - 128) * 192)

# GET newY
def getNew_Y(y, region):
    return 10 * (y - ((region >> 8) - 128) * 192)



log('[%s] Loaded' % __name__)
