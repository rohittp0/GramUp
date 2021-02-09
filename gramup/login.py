#    This is a utility to use Telegram's unlimited storage for backup. 	
#    Copyright (C) 2021  Rohit T P
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see https://www.gnu.org/licenses/

import pickle
import os
from telegram.client import Telegram
from telegram.client import AuthorizationState
try:
	from constants import DATA_FILE,FILES_DIR,API_ID,API_HASH,DATABASE_ENCRYPTION_KEY
except:
	from .constants import DATA_FILE,FILES_DIR,API_ID,API_HASH,DATABASE_ENCRYPTION_KEY
		
def loadData():	 
	try:
		with open(DATA_FILE, "rb") as dbfile:	
			db = pickle.load(dbfile)
			return (db["phone_number"],db["chat_id"],db["back_up_folders"]) 
			
	except Exception as e :
		ph_no = input("Enter your phone number with country code: ")
		bup_folders = set(input("Enter path to folders to be backedup ( seperated by ',' ): ").split(","))
		chat_id = input("Enter the chat ID to be used for backup (leave blank if you are unsure): ") 
		
		if not chat_id.isnumeric() : chat_id = None
		
		os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
		os.makedirs(os.path.dirname(FILES_DIR), exist_ok=True)
		
		with open(DATA_FILE, "wb") as dbfile:
			data = { "phone_number": ph_no, "chat_id": chat_id, "back_up_folders": bup_folders }
			pickle.dump(data, dbfile)
		
		return (ph_no,chat_id,bup_folders)

def login(call_back):
	
	(ph_no,chat_id,bup_folders) = loadData()
	
	tg = Telegram(
			api_id=API_ID,
			api_hash=API_HASH,
			files_directory=FILES_DIR,
			database_encryption_key=DATABASE_ENCRYPTION_KEY,
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
				with open(DATA_FILE, "wb") as dbfile:
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
			
