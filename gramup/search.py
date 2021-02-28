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
import webbrowser
from re import match
from shutil import move
from os.path import join,basename
from tempfile import gettempdir
try :
	from utils import get_messages,download_file
except ImportError :
	from .utils	import get_messages,download_file

def show_file(tg_client,c_file) :
	'''
		This function downloads and displays the file
		with id file_id.
	'''
	(_,file_id,caption) = c_file
	print(f"Downloading {caption}")

	task = download_file(tg_client,file_id)

	if task.error_info is None :
		temp_file = join(gettempdir(),basename(caption))
		move(task.update["local"]["path"],temp_file)
		webbrowser.open(f"file://{temp_file}", new=2)
	else :
		print("Oops... Something went wrong.")

def delete_files(tg_client,chat_id,files) :
	'''
		This function deletes the file with id file_id.
	'''
	if len(files) == 0 :
		return

	print("Are you sure you want to delete,")
	for (_,_,caption_text) in files :
		print(f"  {caption_text}")

	if input("(y/N) ? : ").lower() == "n" :
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
		print("Something went wrong. Please try again")

def search(tg_client,chat_id) :
	'''
		This function searches for uploaded file using the
		RegEx provide by the user.
	'''
	print("You can use Path(Path to file from where it was uploaded) or RegEx to search.")
	print("Enter . to show all files")
	search_reg = input(" : ")

	files = []
	for (msg_id,file_id,caption) in get_messages(tg_client,chat_id) :
		if match(search_reg,caption) :
			files.append((msg_id,file_id,caption))
			print(f"{len(files)}){caption}")

	if len(files) == 0 :
		print("No files matched your search")
	else :
		while True :
			try :
				option = input("View (v) Delete (d) Go Back (b) : ").lower()

				if option == "v" :
					c_file = files[int(input("Enter index of file to open : ")) - 1]
					show_file(tg_client,c_file)
					break
				if option == "d" :
					print("Enter indexes of files seperated by ','")
					indexes = input("Or A (case sensitive) to select all : ").split(",")
					if indexes[0] == "A" :
						delete_files(tg_client,chat_id,files)
					else :
						delete_files(tg_client,chat_id,[ files[ int(i) -1 ] for i in indexes ])
					break
				if option == "b" :
					break

				print("Invalid option")

			except ValueError :
				print("Invalid number")
			except IndexError :
				print("Invalid index")
