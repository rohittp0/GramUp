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
import sys
import pickle
from pathlib import Path
from shutil import rmtree
from enquiries import choose,confirm,freetext
try :
	from constants import MESGS_DIR,CACHE_FILE,DATA_FILE
except ImportError :
	from .constants import MESGS_DIR,CACHE_FILE,DATA_FILE

def clear_cache(_) :
	'''
		This function clears all local caches.
	'''
	if not confirm("Are you sure you want to clear all cache?") :
		return

	rmtree(MESGS_DIR)
	Path(CACHE_FILE).unlink(missing_ok=True)

def change_folder(_) :
	'''
		This function allows user to change backup folder.
	'''
	try:
		with open(DATA_FILE, "rb") as dbfile:
			db_dict = pickle.load(dbfile)

	except FileNotFoundError :
		db_dict = {}

	bup_folders = set(freetext("Enter path to folders to be backedup ( seperated by ',' )").split(","))
	db_dict["back_up_folders"] = bup_folders

	with open(DATA_FILE, "wb") as dbfile:
		pickle.dump(db_dict, dbfile)

def logout(tg_client) :
	'''
		This function logs the user out.
	'''
	if not confirm("Are you sure you want to Logout?") :
		return

	task = tg_client.call_method("logOut",{})
	task.wait()

	if task.error_info :
		print(f"Oops something went wrong\n{task.error_info}")
		return

	rmtree(Path(DATA_FILE).parent)
	freetext("Loged out. Press any enter to exit.")
	sys.exit(0)

def settings(tg_client) :
	'''
		This function displays the settings menu.
	'''
	options = ["Clear Cache","Change Backup Folder","Logout","Go-Back"]
	functions = [ clear_cache, change_folder, logout ]

	while True :
		choise = choose("What do you want to do?", options)

		if options.index(choise) < len(functions) :
			functions[options.index(choise)](tg_client)
		else :
			break
