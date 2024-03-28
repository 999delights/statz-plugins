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

    if get_character_data()['name'] != "":
        character_name = get_startup_data()['character']
        inventory = get_inventory() if get_inventory() is not None else {}
        party = get_party() if get_party() is not None else {}   
        training_area = get_training_area() if get_training_area() is not None else {}
        position = get_position() if get_position() is not None else {}
        job_name = get_character_data()['job_name'] if get_character_data() is not None else ''
        job_mode = get_inventory_job_mode(inventory)
        cast_speed(character_name,position,training_area,party,job_name,job_mode)
       



def cast_speed( name,position,training_area,party,job_name,job_mode):

    
    
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
                if os.path.isfile(file_path) and filename.endswith(".json") and not filename.startswith('condition'):
                     
                    character_name = filename.replace(".json", "")
                    if job_mode != "Not active":
                        adjusted_name = job_name  # or f"{character_name} the {job_mode}" to append
                    else:
                        adjusted_name = name
                    if adjusted_name == character_name: 
                        
                        # Load the JSON content
                        with open(file_path, 'r') as file:
                            data = json.load(file)
                            for key, values in data.items():
                                checked = values.get('checked', False)
                                item_list = values.get('list', [])
                                march = values.get('march',"")
                                is_bard = values.get('isBard', False)
                                main = values.get('main', "")
                            
                                if checked: # if speed is needed
                                    
                                    if not is_bard:  # if not bard
                                        
                                        is_not_found = search_speed()  
                                        
                                        if is_not_found:  # if any speed not found  -
                                            
                                            inParty = party
                                            
                                            if inParty is not Empty:    # if in a party
                                                
                                                
                                                    # First check the priority player
                                                for player_data in party.values():
                                                    player_name = player_data['name']
                                                    if player_name in item_list:
                                                        x = player_data['x']
                                                        y = player_data['y']
                                                        region = player_data['region']
                                                        pos = {'x': x, 'y': y, 'region': region}
                                                        playerInTrainingArea = isInTrainingArea(pos, training_area)
                                                        
                                                        if playerInTrainingArea and isInTrainingArea(position, training_area): # if both in training area
                                                            
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



def handle_chat(t, player, msg):  
    message = str(msg)
    message = urllib.parse.quote(message)
    type = str(messageType(t))
    sender = str(player)
    if type == "party":
        if message == "speeddeeps":



            name = get_startup_data()['character']
            job_name = get_character_data()['job_name'] if get_character_data() is not None else ''
            party = get_party() if get_party() is not None else {}   
            training_area = get_training_area() if get_training_area() is not None else {}
            position = get_position() if get_position() is not None else {}
            playerInTrainingArea = False  # Initialize this to False
            inventory = get_inventory() if get_inventory() is not None else {}
            job_mode = get_inventory_job_mode(inventory)


            # Loop through each file in the directory
            for server_name in os.listdir(speed_dir):
                server_path = os.path.join(speed_dir, server_name)
                if os.path.isdir(server_path):
                    for filename in os.listdir(server_path):
                        # Construct full file path
                        file_path = os.path.join(server_path, filename)
                    
                       
                        # Check if it's a file and has a .json extension
                        if os.path.isfile(file_path) and filename.endswith(".json") and not filename.startswith('condition'):
                            
                            # Extract character name from filename (removing the ".json" part)
                            character_name = filename.replace(".json", "")
                           
                            if job_mode != "Not active":
                                adjusted_name = job_name  # or f"{character_name} the {job_mode}" to append
                            else:
                                adjusted_name = character_name
                            if adjusted_name == name: 
                                
                                # Load the JSON content
                                with open(file_path, 'r') as file:
                                    data = json.load(file)
                                    for key, values in data.items():
                                        checked = values.get('checked', False)
                                        item_list = values.get('list', [])
                                        march = values.get('march',"")
                                        is_bard = values.get('isBard', False)
                                        main = values.get('main', "")
                                        if checked:     # if cast speed is checked 
                                            
                                            if is_bard == True: # if is bard
                                                inParty = party
                                                if inParty is not Empty: 
                                                    if main == "Main":   # if in party
                                                        phBotChat.Party("ok")
                                                        start_script(f'recast,{march}')
                                                    else:
                                                        if item_list is not Empty:          # if other players are prior
                                                            for player_data in inParty.values():
                                                                player_name = player_data['name']
                                                                
                                                                if player_name in item_list:
                                                                    
                                                                    x = player_data['x']
                                                                    y = player_data['y']
                                                                    region = player_data['region']
                                                                    
                                                                    pos = {'x': x, 'y': y, 'region': region}
                                                                    
                                                                    playerInTrainingArea = isInTrainingArea(pos, training_area)
                                                                    if not playerInTrainingArea:
                                                                      inTrainingArea = isInTrainingArea(position, training_area) 
                                                                      if inTrainingArea:
                                                                        phBotChat.Party("ok")
                                                                        start_script(f'recast,{march}')
                                                            
                                                            
                                                                

                                                    

                                
                    
            





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
