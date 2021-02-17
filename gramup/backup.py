'''
    This is a utility to use Telegram's unlimited storage for backup.
    Copyright (C) 2021  Rohit T P

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see https://www.gnu.org/licenses/
'''

from os.path import relpath,basename
from datetime import datetime
from math import ceil
import time
import speedtest

try :
	from utils import get_new_files,get_messages,print_progress_bar
except ImportError :
	from .utils	import get_new_files,get_messages,print_progress_bar

def get_uploaded_files(tg_client,chat_id,parents) :
	'''
		This function returns a list of local paths
		of files that are already uploaded.
	'''
	files = set([])
	table = [(basename(parent),parent) for parent in parents ]

	for (_,caption) in get_messages(tg_client,chat_id) :
		if caption :
			for (base,full) in table :
				if caption.startswith(base) :
					files.add(caption.replace(base,full,1))
					break

	return files

def send_file(tg_client,chat_id,file_path,parent_folder="/") :
	'''
		This function sends the file at file_path to chat with id
		chat_id with path to that file relative to parent_folder
		as the caption.
	'''
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
	return tg_client.call_method("sendMessage",param)

def wait_for_upload(tg_client,msg,net_speed) :
	'''
		This function blocks current thread until a specified
		file has finished uploading.
	'''
	state = msg["sending_state"]["@type"]

	while msg and state == "messageSendingStatePending" :
		left = msg["size"] - msg["remote"]["uploaded_size"]
		time.sleep(ceil(left/net_speed))
		task = tg_client.call_method("getMessage",{"chat_id":msg["chat_id"],"message_id":msg["id"]})
		task.wait()
		msg = task.update["content"]["document"]["document"]
		state = task.update["sending_state"]["@type"]

def show_results(done,failed,errors) :
	'''
		This function prints the result of backup.
	'''
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	print(f"Total files to upload {done+failed}")
	print(f"{done} files uploaded")
	print(f"{failed} files failed to upload")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

	if failed > 0 and input("Do you wan't to see the error log (y/N) ? : ").lower() == "y" :
		print(errors)

def backup(tg_client,chat_id,back_up_folders):
	'''
		This function starts the backup process.
	'''
	print("\nGetting list of uploaded files")
	old_files = get_uploaded_files(tg_client,chat_id,back_up_folders)

	new_files = []
	print("Getting list of files to upload")

	for folder in back_up_folders :
		new_files.extend(get_new_files(folder,old_files))

	if len(new_files) == 0 :
		return show_results(0,0,"")

	print("Measuring internet speed")
	total_files = len(new_files)
	net_speed = speedtest.Speedtest().upload()/8
	(done,failed,errors) = (0,0,"")

	print_progress_bar(0,total_files, autosize = True)
	tg_client.send_message(chat_id=chat_id,text=f"Backup started on {datetime.today().strftime('%Y-%m-%d %I:%M %p')}")
	tg_client.send_message(chat_id=chat_id,text=f"\nBacking up {total_files} files @ {net_speed/1000000} MBps.")

	for (new_file,folder) in new_files :
		task = send_file(tg_client,chat_id,new_file,folder)
		task.wait()
		if task.error_info is None :
			wait_for_upload(tg_client,task.update,net_speed)
			done += 1
		else :
			failed += 1
			errors += str(task.error_info) + "\n\n"
		print_progress_bar(done+failed, total_files, prefix = 'Uploading:', suffix = 'Complete', autosize = True)

	tg_client.send_message(chat_id=chat_id, text=f"Backup ended on {datetime.today().strftime('%Y-%m-%d %I:%M %p')}").wait()

	return show_results(done,failed,errors)
