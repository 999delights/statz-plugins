
from phBot import *
from datetime import datetime
import os
import json
import urllib.parse  # Add this line to import urllib.parse


ready = True










 
def process_tasks_for_character():
    global ready 
    # Get the character's name from get_character_data()
    character_name = get_character_data()['name']
    
    # Define the base directory where messages are stored
    base_dir = r'C:\Users\andre\AppData\Local\Programs\phBot Testing\Plugins\info'

    # Construct the path to the character's message directory
    character_message_dir = os.path.join(base_dir, 'tasks', character_name)
    
    # Check if the character's message directory exists
    if os.path.exists(character_message_dir):
        # Get a list of all JSON files in the directory
        json_files = [f for f in os.listdir(character_message_dir) if f.endswith('.json')]
        
        # Sort the JSON files by modification time (oldest first)
        json_files.sort(key=lambda x: os.path.getmtime(os.path.join(character_message_dir, x)))

        if json_files:
            # Get the path to the oldest JSON file
            oldest_json_file = os.path.join(character_message_dir, json_files[0])

            if os.path.exists(oldest_json_file):  # Check if the file still exists
                # Read the JSON data from the file
                with open(oldest_json_file, 'r') as file:
                    task_data = json.load(file)

                # Delete the oldest JSON file
                os.remove(oldest_json_file)
                
               

        else:
            ready = True  # Set ready to True if no JSON files are found
    else:
        ready = True  # Set ready to True if the message directory doesn't exist






# Event loop
def event_loop():
    global ready
    if get_character_data()['name'] != "":
        if ready == True:
            
        # Add your code here that runs every 5 seconds
            ready = False
            process_tasks_for_character()
            
        # ... (other event loop code)
    




log('[%s] Loaded' % __name__)
