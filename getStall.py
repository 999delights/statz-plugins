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
import re




#1st function 
def create_info_directory():
    directory = 'Plugins/info'
    if not os.path.exists(directory):
        os.makedirs(directory) 


# Function to create the "info" directory if it doesn't exist
def create_info_statz_directory():
    directory = 'Plugins/info/stall'
    if not os.path.exists(directory):
        os.makedirs(directory)


# Function to create the "server" directory if it doesn't exist
def create_server_directory(serverName):
    directory = 'Plugins/info/stall/' + serverName + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)



def parse_log_and_update_stall_data(logs, stall_data, filtered_inventory):
    time = ''
    # Regular expression patterns
    created_pattern = re.compile(r'\[(\d+:\d+:\d+)\] Stall: Stall has been created')
    adding_pattern = re.compile(r'\[(\d+:\d+:\d+)\] Stall: Adding \[(.*?)\] \[(.*?)\] -> \[(.*?)\]')
                            #[23:11:41] Stall: Adding [Drako War God Robe] [1] -> [33,333,333]
    opened_pattern = re.compile(r'\[(\d+:\d+:\d+)\] Stall: Stall has been opened')
    exited_pattern = re.compile(r'\[(\d+:\d+:\d+)\] Stall: Stall has been exited')
    modified_pattern = re.compile(r'\[(\d+:\d+:\d+)\] Stall: Stall is being modified')
    purchased_pattern = re.compile(r'\[(\d+:\d+:\d+)\] Stall: \[(.*?)\] has purchased \[(.*?)\] for \[(.*?)\] gold') 
    # Regular expression patterns                       [23:11:45] Stall: [ginny] has purchased [Jewel Earring] for [12,412] gold
                                                                    #
    log_pattern = re.compile(r'\[(\d+:\d+:\d+)\] Stall: (.*)')
    
    # Parse logs
    for line in logs.split('\n'):
        match = log_pattern.search(line)
        if match:
            if created_pattern.search(line) or modified_pattern.search(line):
                pattern = created_pattern if created_pattern.search(line) else modified_pattern
                time = pattern.search(line).group(1)
                stall_data["state"] = "STALL_MODE"
                stall_data["history"].append({"action": "state_changed" ,"state": "STALL_MODE", "time": time})
                
            elif opened_pattern.search(line):
                time = opened_pattern.search(line).group(1)
                stall_data["state"] = "OPEN"
                stall_data["history"].append({"action": "state_changed" ,"state": "OPEN", "time": time})
                
            elif exited_pattern.search(line):
                time = exited_pattern.search(line).group(1)
                stall_data["state"] = "NOT_IN_STALL_MODE"
                stall_data["history"].append({"action": "state_changed" ,"state": "NOT_IN_STALL_MODE", "time": time})
                # Empty the items_for_sale list when exiting stall mode
                stall_data["items_for_sale"] = []


            elif adding_pattern.search(line):
                 
                
                match = adding_pattern.search(line)
                time, item_name, quantity, price = match.groups()
                # Directly search for the item in the filtered_inventory by its name
                for item in filtered_inventory['items']:
                    if item["name"] == item_name:
                        
                        # Extract additional details from the inventory
                        servername = item.get("servername")
                        model = item.get("model")
                        plus = item.get("plus")
                        
                       
                        # Append item with additional attributes
                        stall_data["items_for_sale"].append({
                            "item": item_name, 
                            "quantity": quantity, 
                            "price": price, 
                            "time": time,
                            "servername": servername,
                            "model": model,
                            "plus": plus
                        })
                        
                        # Record the addition in history with all details
                        stall_data["history"].append({
                            "action": "item_added", 
                            "item": item_name, 
                            "quantity": quantity, 
                            "price": price, 
                            "time": time,
                            "servername": servername,
                            "model": model,
                            "plus": plus
                        })

                        break    

                        
            
        
        
        # Update last_update with the time of the matched pattern
        stall_data["last_update"] = time
          
def event_loop():

    character_name = get_startup_data()['character']
    server_name = get_startup_data()['server']

    create_info_statz_directory() # Create the "info" directory if it doesn't exist
    create_server_directory(server_name)

    filename = 'Plugins/info/stall/'+ server_name + '/stall_'  + character_name +'.json'
   

    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r') as file:
            try:
                stall_data = json.load(file)
            except json.JSONDecodeError:
                log("Error decoding JSON from file: " + filename)
                stall_data = {}
    else:
        stall_data = {
                    
                    }   
    

    inventory = get_inventory() if get_inventory() is not None else {}
    filtered_inventory = {
    "items": [
        item for item in inventory["items"][13:] if item is not None
    ] if "items" in inventory else []
}


    
    logs = get_log() if get_log() is not None else ""

    stall_data = {
                                "state": "NOT_IN_STALL_MODE",  # Current state of the stall
                                "history": [],  # History of state changes and events
                                "items_for_sale": [],  # Items currently for sale (max 10)
                                "sold_items": [],  # List of sold items (no max)
                                "last_update": ""  # Last update time
                                }   
    
    
    parse_log_and_update_stall_data(logs, stall_data, filtered_inventory)
    # Ensure 'items_for_sale' list is exactly 10 elements long by filling with None if necessary
    while len(stall_data["items_for_sale"]) < 10:
        stall_data["items_for_sale"].append(None)
    stall = {}
    stall[f"{character_name}/{server_name}"] = {"stall": stall_data}
    
    # Export the updated dictionary to the JSON file for each character in the info dir 
    with open(filename, 'w') as file:     
        json.dump(stall, file, indent=4)


            


log('[%s] Loaded' % __name__)
