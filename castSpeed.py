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





PRIORITY_PLAYER = ["GWEN", "ginny"]
CHARACTER_NAMES = ["Drea", "Candace", "JUMPMAN", "MikeOxlong"]




def event_loop():

    if get_character_data()['name'] != "":
        character_name = get_startup_data()['character']
        
        party = get_party() if get_party() is not None else {}   
        training_area = get_training_area() if get_training_area() is not None else {}
        position = get_position() if get_position() is not None else {}
        
        cast_speed(character_name,position,training_area,party)
       



def cast_speed( name,position,training_area,party):

    # Directory where JSON files are stored
    speed_dir = r'C:\Users\andre\AppData\Local\Programs\phBot Testing\Plugins\info\tasks\speed'
    
    # Check if the directory exists
    if not os.path.exists(speed_dir):
        log("The directory" + speed_dir +" does not exist!")
        return

    # Loop through each file in the directory
    for filename in os.listdir(speed_dir):
        # Construct full file path
        file_path = os.path.join(speed_dir, filename)
       
        # Check if it's a file and has a .json extension
        if os.path.isfile(file_path) and filename.endswith(".json"):
                
            # Extract character name from filename (removing the ".json" part)
            character_name = filename.replace(".json", "")
            
            if character_name == name: 
                
                # Load the JSON content
                with open(file_path, 'r') as file:
                    data = json.load(file)
                
                    # Extract the required data
                    checked = data["checked"]
                    isBard =  data['isBard']
                    
                    if checked: # if speed is needed
                        
                        if not isBard:  # if not bard
                            
                            is_not_found = search_speed()  
                            
                            if is_not_found:  # if any speed not found  -
                                
                                inParty = party
                                
                                if inParty is not Empty:    # if in a party
                                    
                                        # First check the priority player
                                    for player_data in party.values():
                                        player_name = player_data['name']
                                        if player_name in PRIORITY_PLAYER:
                                            x = player_data['x']
                                            y = player_data['y']
                                            region = player_data['region']
                                            pos = {'x': x, 'y': y, 'region': region}
                                            playerInTrainingArea = isInTrainingArea(pos, training_area)
                                            
                                            if playerInTrainingArea and isInTrainingArea(position, training_area): # if both in training area
                                                
                                                return phBotChat.Party("speeddeeps")
                                                # return from the function as soon as priority player is found in the area
                                    
                                    # Then check the rest of the players
                                    for player_data in party.values():
                                        player_name = player_data['name']
                                        if player_name in CHARACTER_NAMES:
                                            x = player_data['x']
                                            y = player_data['y']
                                            region = player_data['region']
                                            pos = {'x': x, 'y': y, 'region': region}
                                            playerInTrainingArea = isInTrainingArea(pos, training_area)
                                            
                                            if playerInTrainingArea and isInTrainingArea(position, training_area):
                                                
                                                return phBotChat.Party("speeddeeps")
                                                
                                    

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
        name = get_startup_data()['character']
        party = get_party() if get_party() is not None else {}   
        training_area = get_training_area() if get_training_area() is not None else {}
        position = get_position() if get_position() is not None else {}
       
        playerInTrainingArea = False  # Initialize this to False
        if message == "speeddeeps":
            speed_dir = r'C:\Users\andre\AppData\Local\Programs\phBot Testing\Plugins\info\tasks\speed'
            # Loop through each file in the directory
            for filename in os.listdir(speed_dir):
                # Construct full file path
                file_path = os.path.join(speed_dir, filename)
               
                # Check if it's a file and has a .json extension
                if os.path.isfile(file_path) and filename.endswith(".json"):
                    
                    # Extract character name from filename (removing the ".json" part)
                    character_name = filename.replace(".json", "")
                    
                    if character_name == name: 
                        
                        # Load the JSON content
                        with open(file_path, 'r') as file:
                            data = json.load(file)
                        
                            # Extract the required data
                            checked = data["checked"]
                            players = data["players"]
                            isBard =  data['isBard']
                            if checked:     # if cast speed is checked 
                                
                                if isBard == True: # if is bard
                                    inParty = party
                                    if inParty is not Empty:      # if in party
                                        if players is not Empty:          # if other players are prior
                                            for player_data in inParty.values():
                                                player_name = player_data['name']
                                                
                                                if player_name in players:
                                                    
                                                    x = player_data['x']
                                                    y = player_data['y']
                                                    region = player_data['region']
                                                    
                                                    pos = {'x': x, 'y': y, 'region': region}
                                                    
                                                    playerInTrainingArea = isInTrainingArea(pos, training_area)
                                                    if playerInTrainingArea:
                                                        break  # Exit the loop once we find a player in the training area
                                                        
                                            if not playerInTrainingArea:     
                                               
                                                inTrainingArea = isInTrainingArea(position, training_area)
                                              
                                                if inTrainingArea:
                                                    start_script('recast,Swing March')

                                                

                                
                    
            





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
