from phBot import *
import phBotChat
import datetime


def handle_chat(t,player,msg):
	type = 'None'
	if t ==5:
		type = '(Guild)'
	if t == 11:
		type = '(Union)'
	if type != 'None':
		file = open("Log/chat/"+get_character_data()['server']+"_"+get_character_data()['name']+"_ChatLogGuild&Union.txt","a")
		date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
		file.write('['+date+']'+type+player+': '+msg+'\n')
		file.close()
		
log('[%s] Loaded' % __name__)



