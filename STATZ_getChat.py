
from http import server
from phBot import *
import phBotChat
from datetime import datetime
import os
import json
import urllib.parse  # Add this line to import urllib.parse


ready = True
last_update_date = None

#1st function 
def create_info_directory():
    directory = 'Plugins/info'
    if not os.path.exists(directory):
        os.makedirs(directory) 


def create_messages_directory():
    directory = 'Plugins/info/messages'
    if not os.path.exists(directory):
        os.makedirs(directory) 

def create_directories():
     # Main directory path
    main_directory_path = r'C:\Users\andre\AppData\Local\Programs\phBot Testing\Plugins\info\messages'
    # Additional directories
    msgs_directory = main_directory_path + r'\msgs'
    LIVE_directory = main_directory_path + r'\LIVE'

    if not os.path.exists(msgs_directory):
        os.makedirs(msgs_directory)
    if not os.path.exists(LIVE_directory):
        os.makedirs(LIVE_directory)


create_directories()

def calculate_threshold_date(current_date):
    THRESHOLD_DAYS = 2

    # Extract the year, month, and day from the current date
    year, month, day = current_date.year, current_date.month, current_date.day

    # Subtract THRESHOLD_DAYS from the day, handling month/year changes
    for _ in range(THRESHOLD_DAYS):
        day -= 1
        if day == 0:
            month -= 1
            if month == 0:
                year -= 1
                month = 12
            # Calculate the number of days in the previous month
            days_in_previous_month = {
                1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
                7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
            }.get(month, 0)

            day = days_in_previous_month

    # Return the calculated threshold date as a string in the format "DD/MM/YYYY"
    return f"{day:02d}/{month:02d}/{year}"



def compare_date_strings(date_str1, date_str2):
    # Split date strings into parts
    parts1 = date_str1.split("/")
    parts2 = date_str2.split("/")

    if parts1[2] < parts2[2]:
        return False
    elif parts1[1] > parts2[1]:
        return True
    elif parts1[1] < parts2[1]:
        return False
    elif parts1[0] >= parts2[0]:
        return True
    else:
        return False


# Messages
class Message:
    def __init__(self, message, player, type, date, way):
        self.message = message
        self.player = player
        self.type = type
        self.date = date
        self.way = way

    def toDict(self):
      return {"message": self.message, "player": self.player, "type": self.type, "date": self.date, "way": self.way}



# Function to check if a message is spam (you can define your own criteria)
def is_message_spam(_m):
    # Check if the message type is "General"
    if _m.type == "General":
        # Get the character's name and server
        character_name = get_character_data()['name']
        server_name = get_character_data()['server']

         # Define the directory path for the server's message directory
        server_dir = 'Plugins/info/messages/msgs/' + server_name

        # If the server directory doesn't exist, create it
        if not os.path.exists(server_dir):
            os.makedirs(server_dir)

        # Define the file path for the JSON file
        file_path = 'Plugins/info/messages/msgs/' + server_name + '/' + character_name + '.json'

        # Check if the JSON file already exists
        if os.path.exists(file_path):
            # Read the existing JSON data from the file
            with open(file_path, 'r') as file:
                info_data = json.load(file)

            # Check if the character already has "General" messages
            if f"{character_name}/{server_name}" in info_data and 'msgs' in info_data[f"{character_name}/{server_name}"]:
                # Get the list of "General" messages
                general_msgs = [msg['message'] for msg in info_data[f"{character_name}/{server_name}"]['msgs'] if msg['type'] == 'General']

                # Check if the new "General" message is the same as the last uploaded one
                if general_msgs and general_msgs[-1] == _m.message:
                    # If it's the same as the last uploaded, consider it spam
                    return True

    # For message types other than "General," assume it's not spam
    return False




#Message type
def messageType(type):
    if type == 1:
        return "general"
    elif type == 2:
        return "private"
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

# Send PM
def sendPM(message, to, player):
    
    if to == 'party':
        return phBotChat.Party(message)
    elif to == 'guild':
        return phBotChat.Guild(message)
    elif to == 'union':
        return phBotChat.Union(message)
    elif to == 'stall':
        return phBotChat.Stall(message)
    elif to == 'global':
        return phBotChat.Global(message)
    elif to == 'academy':
        return phBotChat.Academy(message)
    elif to == 'note':
        return phBotChat.Note(player,message)
    elif to == 'private':
        return phBotChat.Private(player, message)
    else:
        return phBotChat.All(message)





def update_messages_with_threshold():

   # Get the character's name and server
    character_name = get_character_data()['name']
    server_name = get_character_data()['server']


    # Define the directory path for the server's message directory
    server_dir = 'Plugins/info/messages/msgs/' + server_name

    # If the server directory doesn't exist, create it
    if not os.path.exists(server_dir):
        os.makedirs(server_dir)

    # Define the file paths for the JSON files
    file_path_to = 'Plugins/info/messages/msgs/' + server_name + '/to_' + character_name + '.json'
    file_path_normal = 'Plugins/info/messages/msgs/' + server_name + '/' + character_name + '.json'

    # Calculate the threshold date (current date minus THRESHOLD_DAYS)
    threshold_date_str = calculate_threshold_date(datetime.now())

    # Initialize lists to store passed messages
    passed_msgs_to = []
    passed_msgs_normal = []

    # Check if the file with TO messages exists
    if os.path.exists(file_path_to):
        # Read the existing JSON data from the TO file
        with open(file_path_to, 'r') as file:
            to_info_data = json.load(file)

        # Iterate through the TO messages for the character
        if f"{character_name}/{server_name}" in to_info_data:
            for msg in to_info_data[f"{character_name}/{server_name}"]['dmTOmsgs']:
                date_str = msg['date']
                formatted_date = date_str.split(" ")[0]
                # Compare the date strings with the threshold date
                if compare_date_strings(formatted_date, threshold_date_str):
                    passed_msgs_to.append(msg)

    # Check if the normal file exists
    if os.path.exists(file_path_normal):
        # Read the existing JSON data from the normal file
        with open(file_path_normal, 'r') as file:
            normal_info_data = json.load(file)

        # Iterate through the normal messages for the character
        if f"{character_name}/{server_name}" in normal_info_data:
            for msg in normal_info_data[f"{character_name}/{server_name}"]['msgs']:
                date_str = msg['date']
                formatted_date = date_str.split(" ")[0]
                # Compare the date strings with the threshold date
                if compare_date_strings(formatted_date, threshold_date_str):
                    passed_msgs_normal.append(msg)

    # Update TO messages file with passed messages
    with open(file_path_to, 'w') as file:
        json.dump({f"{character_name}/{server_name}": {'dmTOmsgs': passed_msgs_to}}, file, indent=4)

    # Update normal messages file with passed messages
    with open(file_path_normal, 'w') as file:
        json.dump({f"{character_name}/{server_name}": {'msgs': passed_msgs_normal}}, file, indent=4)










# Function to update message data in JSON file
def update_message_private_TO_data(_m):

    # Get the character's name and server
    character_name = get_character_data()['name']
    server_name = get_character_data()['server']

    # Define the directory path for the server's message directory
    server_dir = 'Plugins/info/messages/msgs/' + server_name

    # If the server directory doesn't exist, create it
    if not os.path.exists(server_dir):
        os.makedirs(server_dir)

    # Define the file path for the JSON file
    file_path = 'Plugins/info/messages/msgs/' + server_name + '/to_'  + character_name + '.json'

    # Check if the JSON file already exists
    if os.path.exists(file_path):
        # Read the existing JSON data from the file
        with open(file_path, 'r') as file:
            info_data = json.load(file)
    else:
        # If the file doesn't exist, create an empty dictionary
        info_data = {}


    # Calculate the threshold date (current date minus THRESHOLD_DAYS)
    current_date = datetime.now()
    threshold_date_str = calculate_threshold_date(current_date)

    # Initialize a list to store messages that are not older than the threshold date
    filtered_msgs = []
    # Check if the character already has messages
    if f"{character_name}/{server_name}" in info_data:
        # Iterate through the character's existing messages
        for msg in info_data[f"{character_name}/{server_name}"]['dmTOmsgs']:
           
            date_str = msg['date']
            formatted_date =  date_str.split(" ")[0]
    
           # Compare the date strings
            if compare_date_strings(formatted_date,threshold_date_str):
                filtered_msgs.append(msg)
                
    
    # Add the new message data to the list
    filtered_msgs.append(_m.toDict())

    # Update the character's messages
    info_data[f"{character_name}/{server_name}"] = {'dmTOmsgs': filtered_msgs}

 # Write the updated data back to the JSON file
    with open(file_path, 'w') as file:
        json.dump(info_data, file, indent=4)


# Function to update message data in JSON file
def update_message_data(_m):



    # Get the character's name and server
    character_name = get_character_data()['name']
    server_name = get_character_data()['server']


    # Define the directory path for the server's message directory
    server_dir = 'Plugins/info/messages/msgs/' + server_name

    # If the server directory doesn't exist, create it
    if not os.path.exists(server_dir):
        os.makedirs(server_dir)

    # Define the file path for the JSON file
    file_path = 'Plugins/info/messages/msgs/' + server_name + '/' + character_name + '.json'

    # Check if the JSON file already exists
    if os.path.exists(file_path):
        # Read the existing JSON data from the file
        with open(file_path, 'r') as file:
            info_data = json.load(file)
    else:
        # If the file doesn't exist, create an empty dictionary
        info_data = {}


    # Calculate the threshold date (current date minus THRESHOLD_DAYS)
    current_date = datetime.now()
    threshold_date_str = calculate_threshold_date(current_date)

    # Initialize a list to store messages that are not older than the threshold date
    filtered_msgs = []

    # Check if the character already has messages
    if f"{character_name}/{server_name}" in info_data:
        # Iterate through the character's existing messages
        for msg in info_data[f"{character_name}/{server_name}"]['msgs']:
            date_str = msg['date']
            formatted_date =  date_str.split(" ")[0]
            
            # Compare the date strings
            if compare_date_strings(formatted_date, threshold_date_str):
                filtered_msgs.append(msg)
    
    # Check if the new message is spam (you can define your own criteria for spam detection)
    if not is_message_spam(_m):
        # Add the new message data to the list
        filtered_msgs.append(_m.toDict())

        # Update the character's messages
        info_data[f"{character_name}/{server_name}"] = {'msgs': filtered_msgs}

        # Write the updated data back to the JSON file
        with open(file_path, 'w') as file:
            json.dump(info_data, file, indent=4)

 
def process_messages_for_character():
    global ready 
    # Get the character's name and server
    character_name = get_character_data()['name']
    server_name = get_character_data()['server']

    
    # Define the directory path for the server's message directory
    server_dir = 'Plugins/info/messages/LIVE/' + server_name

    # If the server directory doesn't exist, create it
    if not os.path.exists(server_dir):
        os.makedirs(server_dir)
    
    # Define the base directory where messages are stored
    base_dir = r'C:\Users\andre\AppData\Local\Programs\phBot Testing\Plugins\info\messages'

    # Construct the path to the character's message directory within the server's directory
    character_events_dir = os.path.join(base_dir, 'LIVE', server_name, character_name)

    
    # Check if the character's message directory exists
    if os.path.exists(character_events_dir):
        # Get a list of all JSON files in the directory
        json_files = [f for f in os.listdir(character_events_dir) if f.endswith('.json')]
        
        # Sort the JSON files by modification time (oldest first)
        json_files.sort(key=lambda x: os.path.getmtime(os.path.join(character_events_dir, x)))

        if json_files:
            # Get the path to the oldest JSON file
            oldest_json_file = os.path.join(character_events_dir, json_files[0])

            if os.path.exists(oldest_json_file):  # Check if the file still exists
                # Read the JSON data from the file
                with open(oldest_json_file, 'r') as file:
                    message_data = json.load(file)

                # Delete the oldest JSON file
                os.remove(oldest_json_file)
                
                # Extract message details
                message = message_data.get('message', '')
                to = message_data.get('to', '')
                player = message_data.get('player', '')
             
                if message and to:
                    # Send the message using sendPM and wait for a response
                    response_received = sendPM(message, to, player)
                    log('Try to send: ' + message)
                    
                    if response_received == True:
                        # If the response is true, update the message data
                        # true even if the player is offline , should look for the opCODE 
                        sender = player
                        type = to
                        current_date = datetime.now()
                        
                        #decoded_message2 = message.encode('utf-8').decode('unicode_escape')
                        if type == 'private':
                            way = "(TO)"
                            _m = Message(message, sender, type, current_date.strftime("%d/%m/%Y %H:%M:%S"), way)
                            # Call the function to update message data in JSON file
                            ready = True
                            update_message_private_TO_data(_m)
                            

                        else:
                            ready = True

                    else:
                        ready = True

                else:
                    ready = True
        else:
            ready = True  # Set ready to True if no JSON files are found
    else:
        ready = True  # Set ready to True if the message directory doesn't exist


		# Chat message received
def handle_chat(t, player, msg):  
    message = str(msg)
    message = urllib.parse.quote(message)
    currentDate = datetime.now()
    type = str(messageType(t))
    sender = str(player)
    way = ""

    if type == "private":
        way = "(FROM)"
 
    
    if message != "speeddeeps":
        # Create a dictionary to store the message data
        _m = Message(message, sender, type, currentDate.strftime("%d/%m/%Y %H:%M:%S"), way)
        
        # Call the function to update message data in JSON file
        update_message_data(_m)




# Event loop
def event_loop():
    global ready, last_update_date
    if get_character_data()['name'] != "":
        # Get today's date (without time part)
        today = datetime.now().date()
        
        # Check if update_messages_with_threshold has not been done today
        if last_update_date is None or last_update_date != today:
            update_messages_with_threshold()
            last_update_date = today  # Update the last update date to today    
        if ready == True:
            
            ready = False
            process_messages_for_character()
             
        # ... (other event loop code)
    




log('[%s] Loaded' % __name__)
