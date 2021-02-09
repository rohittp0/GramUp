from datetime import datetime
from os.path import relpath
from pathlib import Path
import speedtest
import utils
import time

def getUploadedFiles(tg,chat_id) :	
	last_id = 0
	files = set([])
	
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
				files.add(message["content"]["document"]["document"]["local"]["path"])
			last_id = message["id"]
	
	return files

def sendFile(tg,chat_id,file_path,parent_folder="/") :
		param= {
			'chat_id': chat_id,
			'input_message_content': {
				'@type':'inputMessageDocument',
				'document': {
					'@type':'inputFileLocal',
					'path': file_path
				},
				'caption' : {
					'@type': 'formattedText', 
					'text': str(relpath(file_path,parent_folder))
				},
				'disable_content_type_detection': True
			},
			'@extra': {
				'path': file_path
			}
		}
		return tg.call_method("sendMessage",param)
		
def showResults(done,failed,errors) :
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	print(f"Total files to upload {total_files}")
	print(f"{done} files uploaded")
	print(f"{failed} files failed to upload")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~") 
	
	tg.send_message(chat_id=chat_id, text=f"Backup ended on {datetime.today().strftime('%Y-%m-%d %I:%M %p')}");
	
	if failed > 0 and input("Do you wan't to see the error log (y/N) ? : ").lower() == "y" :
		print(errors) 
	
	print("\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
	print("Press crtl+c once you recive all files\n\n") 
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
	
	return None	
		
def backup(tg,chat_id,back_up_folders):
	print("\nGetting list of uploaded files")
	old_files = getUploadedFiles(tg,chat_id)
	
	new_files = []
	print("Getting list of files to upload")
	
	for folder in back_up_folders :
		new_files.extend(utils.getNewFiles(folder,old_files))
	
	if len(new_files) == 0 : return showResults(0,0,"")	
		
	print("Measuring internet speed")	
	total_files = len(new_files)
	net_speed = speedtest.Speedtest().upload()/8
	(done,failed,errors) = (0,0,"")
	
	utils.printProgressBar(0,total_files, autosize = True)	
	tg.send_message(chat_id=chat_id,text=f"Backup started on {datetime.today().strftime('%Y-%m-%d %I:%M %p')}")
	tg.send_message(chat_id=chat_id,text=f"\nBacking up {total_files} files @ {net_speed/1000000} MBps.");
		
	for (new_file,folder) in new_files : 
		task = sendFile(tg,chat_id,new_file,folder)
		task.wait();
		if(task.error_info == None ) : 
			time.sleep(task.update["content"]["document"]["document"]["size"]/net_speed)   
			done += 1
		else :
			failed += 1
			errors += str(task.error_info) + "\n\n"
		utils.printProgressBar(done+failed, total_files, prefix = 'Uploading:', suffix = 'Complete', autosize = True)
		
	showResults(done,failed,errors)		   
	tg.idle()
