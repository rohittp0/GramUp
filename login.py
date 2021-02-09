import pickle
import constants
import os
from telegram.client import Telegram
from telegram.client import AuthorizationState

def loadData():	 
	try:
		with open(constants.DATA_FILE, "rb") as dbfile:	
			db = pickle.load(dbfile)
			return (db["phone_number"],db["chat_id"],db["back_up_folders"]) 
			
	except Exception as e :
		ph_no = input("Enter your phone number with country code: ")
		bup_folders = set(input("Enter path to folders to be backedup ( seperated by ',' ): ").split(","))
		chat_id = input("Enter the chat ID to be used for backup (leave blank if you are unsure): ") 
		
		if not chat_id.isnumeric() : chat_id = None
		
		os.makedirs(os.path.dirname(constants.DATA_FILE), exist_ok=True)
		os.makedirs(os.path.dirname(constants.FILES_DIR), exist_ok=True)
		
		with open(constants.DATA_FILE, "wb") as dbfile:
			data = { "phone_number": phone_number, "chat_id": chat_id, "back_up_folders": bup_folders }
			pickle.dump(data, dbfile)
		
		return (ph_no,chat_id,bup_folders)

def login(call_back):
	
	(ph_no,chat_id,bup_folders) = loadData()
	
	tg = Telegram(
			api_id=constants.API_ID,
			api_hash=constants.API_HASH,
			files_directory=constants.FILES_DIR,
			database_encryption_key=constants.DATABASE_ENCRYPTION_KEY,
			tdlib_verbosity=0,
			phone=ph_no
		)
	
	tg.call_method(
		'setOption',
		{
			'name': 'prefer_ipv6',
			'value': {'@type': 'optionValueBoolean', 'value': False},
		},
	)
	
	tg.login()
	tg.get_chats().wait()	
	
	if chat_id == None :
		def messageHandler(update) :	 	
			message_content = update['message']['content'].get('text', {})
			message_text = message_content.get('text', '').lower()
		
			if message_text == 'use_this_chat':
				with open(constants.DATA_FILE, "wb") as dbfile:
					pickle.dump(
						{ 
							"phone_number": ph_no, 
							"chat_id": update['message']['chat_id'], 
							"back_up_folders": bup_folders 
						}, 
						dbfile
					)
						
				tg.send_message(
					chat_id=chat_id,
					text='Chat selected for backup. \nIf this was not the first time then restart app.'
				)	
									
				call_back(tg,chat_id,bup_folders)
		tg.add_message_handler(messageHandler)
		print("Send 'use_this_chat' to the chat you wan't to use for backup (case insensitive)")
		tg.idle()  # blocking waiting for CTRL+C
	
	call_back(tg,chat_id,bup_folders)
			
