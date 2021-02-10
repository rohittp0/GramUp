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

from shutil import copyfile,rmtree
from os.path import join,dirname,isfile
from os import makedirs
try :
	from constants import RE_FOLDER,MESGS_DIR
	from utils import printProgressBar
except :
	from .constants import RE_FOLDER,MESGS_DIR
	from .utils import printProgressBar	
	
def getUploadedFiles(tg,chat_id) :	
	last_id = 0
	files = []
	
	while True :
		messages = tg.call_method(
			"getChatHistory",
			{
				"chat_id": chat_id,
				"offset": 0,
				"limit": 100,
				"only_local": False,
				"from_message_id": last_id
			}
		)
		
		messages.wait()
		if len(messages.update["messages"]) == 0 : break
		for message in messages.update["messages"] :
			if "document" in message["content"] and message["content"]["document"]["document"]["local"]["can_be_downloaded"] :
				files.append((message["content"]["document"]["document"]["id"],message["content"]["caption"]["text"]))
			last_id = message["id"]
	
	return files
	
def downloadFiles(tg,files) :
	(restored,failed,total) = (0,0,len(files))
	errors = ""
	
	if total <= 0 : return (restored,failed,errors)
	
	printProgressBar(0,total, autosize = True)
	
	for (file_id,path) in files :
		
		if isfile(join(RE_FOLDER,path)) : 
			restored+=1
			printProgressBar(restored+failed, total, prefix = 'Restoring:', suffix = 'Complete', autosize = True)
			continue
			
		task = tg.call_method("downloadFile",
			{
				"file_id": file_id,
				"priority": 32,
				"offset": 0,
				"limit": 0,
				"synchronous": True
			}
		)
		task.wait()
		if not path : path = str(file_id)
		if task.error_info == None :
			makedirs(dirname(join(RE_FOLDER,path)), exist_ok=True)	
			copyfile(task.update["local"]["path"],join(RE_FOLDER,path))
			restored += 1
		else : 
			errors += str(task.error_info) + "\n"
			failed += 1
		printProgressBar(restored+failed, total, prefix = 'Restoring:', suffix = 'Complete', autosize = True)
		
	return (restored,failed,errors)				   

def restore(tg,chat_id) :
	print("\nGetting file list")
	files = getUploadedFiles(tg,chat_id)
	
	print(f"Restoring {len(files)} files\n")
	(restored,failed,errors) = downloadFiles(tg,files)
	
	print("\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
	print(f"{restored} files restored to ~/Restored")
	print(f"{failed} failed \n")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
	
	rmtree(MESGS_DIR)
	
	if failed > 0 and input("Do you wan't to see the error log (y/N) ? : ").lower() == "y" :
		print(errors)
			
