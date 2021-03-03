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
import pickle
import webbrowser
from shutil import move
from re import error as re_error
from re import search as re_search
from tempfile import gettempdir
from os.path import join,basename
from enquiries import choose,freetext

try :
	from constants import CACHE_FILE
	from utils import get_messages,download_file
except ImportError :
	from .constants import CACHE_FILE
	from .utils	import get_messages,download_file

def show_file(tg_client,files) :
	'''
		This function downloads and displays the file
		with id file_id.
	'''
	for (_,file_id,caption) in files :

		task = download_file(tg_client,file_id)

		if task.error_info is None :
			temp_file = join(gettempdir(),basename(caption))
			move(task.update["local"]["path"],temp_file)
			webbrowser.open(f"file://{temp_file}", new=2)
		else :
			print(f"Oops... Something went wrong.\n{task.error_info}")

def delete_files(tg_client,chat_id,files) :
	'''
		This function deletes the file with id file_id.
	'''
	if len(files) == 0 :
		return

	question = "\n".join([ f"  {caption_text}" for (_,_,caption_text) in files ])
	question += "\n\nAre you sure you want to delete these files?"

	if choose(question,["Yes", "No"]) == "No" :
		return

	task = tg_client.call_method("deleteMessages",
		{
			"chat_id": chat_id,
			"message_ids": [ msg_id for (msg_id,_,_) in files ],
			"revoke": True
		}
	)

	print("Deleting... Please wait.")
	task.wait()

	if task.error_info :
		print(f"Oops... Something went wrong.\n{task.error_info}")
	else :
		with open(CACHE_FILE, "wb") as dbfile:
			pickle.dump(list(set(get_messages(tg_client,chat_id))-set(files)), dbfile)

def search(tg_client,chat_id) :
	'''
		This function searches for uploaded file using the
		RegEx provide by the user.
	'''
	search_reg = freetext("Enter the file path to search for ( RegEx supported )")
	files = []

	for (msg_id,file_id,caption) in get_messages(tg_client,chat_id) :
		try :
			if re_search(search_reg,caption) :
				files.append((msg_id,file_id,caption))
				print(f"{len(files)}){caption}")
		except re_error:
			pass

	print()

	if len(files) == 0 :
		return freetext("No files matched your search")

	options = ["View", "Delete", "Go Back"]

	while True :
		try :
			choise = choose("What do you want to do?", options)
			if choise == options[2] :
				break

			if len(files) == 1 :
				selected = files
			else :
				indexes = freetext("Enter indexes of files seperated by ',' or A to select all").split(",")
				selected = files if indexes[0].lower() == "a" else [ files[ int(i.strip()) -1 ] for i in indexes ]

			if choise == options[0] :
				show_file(tg_client,selected)

			elif choise == options[1] :
				delete_files(tg_client,chat_id,selected)

		except ( ValueError,IndexError ) :
			print(f"Please enter number between 1 and {len(files)}")

	return None
