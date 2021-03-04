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
from os import system
from shutil import get_terminal_size
from pathlib import Path
try:
	from constants import CACHE_FILE
	from __init__ import BANNER
except ImportError:
	from .constants import CACHE_FILE
	from .__init__ import BANNER

def print_banner() :
	'''
		This function prints the GramUp banner.
	'''
	system('cls||clear')
	print(BANNER)

def download_file(tg_client,file_id) :
	'''
		This function downloads the file with given file id.
	'''
	task = tg_client.call_method("downloadFile",
			{
				"file_id": file_id,
				"priority": 32,
				"offset": 0,
				"limit": 0,
				"synchronous": True
			}
		)
	task.wait()

	return task

def get_messages(tg_client,chat_id) :
	'''
		This function gets all messages from a chat.
	'''
	errors = 0

	try:
		with open(CACHE_FILE, "rb") as dbfile:
			all_messages = pickle.load(dbfile)
			(last_id,_,_) = all_messages[-1]

	except (FileNotFoundError,EOFError) :
		all_messages = []
		last_id = 0

	while True :
		messages = tg_client.call_method(
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
		try :
			if not messages.update["messages"] or not len(messages.update["messages"]) > 0  :
				break

			for message in messages.update["messages"] :
				if "document" in message["content"] :
					if message["content"]["document"]["document"]["local"]["can_be_downloaded"] :
						all_messages.append((
							message["id"],
							message["content"]["document"]["document"]["id"],
							message["content"]["caption"]["text"]
						))

			last_id = messages.update["messages"][-1]["id"]
			errors = 0

		except TypeError :
			errors += 1
			if errors > 10 :
				print("Too many errors. Try again later.")
				sys.exit(errors)

	with open(CACHE_FILE, "wb") as dbfile:
		pickle.dump(all_messages, dbfile)

	return all_messages

def get_new_files(root,old_files) :
	'''
		Returns the list of files in root directories that are
		not in old_files.
	'''
	files = set([])
	grandparent = Path(root).parent

	for path in Path(root).rglob('*') :
		if path.is_file() :
			files.add(str(path))

	return [(item,grandparent) for item in files - old_files]

def print_progress_bar (iteration, total, prefix = '', suffix = '', fill = '█'):
	'''
	Call in a loop to create terminal progress bar
	@params:
		iteration   - Required  : current iteration (Int)
		total	   - Required  : total iterations (Int)
		prefix	  - Optional  : prefix string (Str)
		suffix	  - Optional  : suffix string (Str)
		fill		- Optional  : bar fill character (Str)
	'''
	percent = ("{0:." + str(1) + "f}").format(100 * (iteration / float(total)))
	styling = '%s |%s| %s%% %s' % (prefix, fill, percent, suffix)
	cols, _ = get_terminal_size(fallback = (100, 1))
	length = cols - len(styling)
	filled_length = int(length * iteration // total)
	p_bar = fill * filled_length + '-' * (length - filled_length)
	print('\r%s' % styling.replace(fill, p_bar), end = '\r')
	# Print New Line on Complete
	if iteration == total:
		print()
