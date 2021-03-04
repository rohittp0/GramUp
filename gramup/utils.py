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
import logging
from os import system
from shutil import get_terminal_size
from pathlib import Path
try:
	from constants import CACHE_FILE,LOG_FILE
	from __init__ import BANNER
except ImportError:
	from .constants import CACHE_FILE,LOG_FILE
	from .__init__ import BANNER

def get_logger() :
	'''
		This enables logging to log file.
	'''
	logging.basicConfig(
		filename=LOG_FILE,
		level=logging.INFO,
		format='%(asctime)s %(levelname)s %(name)s %(message)s'
	)

	return logging.getLogger(__name__)

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

def get_file_id(tg_client,chat_id,msg_id) :
	'''
		This function gets the file id using message id.
	'''
	msg = tg_client.call_method("getMessage",
		{
			"chat_id": chat_id,
			"message_id": msg_id
		}
	)
	msg.wait()

	if msg.error_info :
		get_logger().error("Error getting file id %s",msg.error_info)
		return None

	msg = msg.update["content"]

	if "document" in msg and msg["document"]["document"]["local"]["can_be_downloaded"] :
		return msg["document"]["document"]["id"]

	return None

def get_messages(tg_client,chat_id) :
	'''
		This function gets all messages from a chat.
	'''
	errors = 0
	file_log = get_logger()

	try:
		with open(CACHE_FILE, "rb") as dbfile:
			all_messages,last_id = pickle.load(dbfile)

		file_log.info("Read %s messages from cache. Last id %s", len(all_messages),last_id)

	except (FileNotFoundError,EOFError) as f_er :
		( all_messages, last_id ) = ( set([]), 0 )
		file_log.warning("No cache found %s",f_er)

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
						all_messages.add((
							message["id"],
							message["content"]["document"]["document"]["id"],
							message["content"]["caption"]["text"]
						))

			last_id = messages.update["messages"][-1]["id"]
			errors = 0

		except TypeError as t_er:
			errors += 1
			file_log.warning("Error getting messages %s",t_er)
			if errors > 10 :
				print("Too many errors. Try again later.")
				file_log.error("Too many errors %s", messages.error_info)
				sys.exit(errors)

	file_log.info("Got %s messages in total", len(all_messages))

	with open(CACHE_FILE, "wb") as dbfile:
		pickle.dump(({ (m_id,None,cap_txt) for (m_id,_,cap_txt) in all_messages }, last_id), dbfile)

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
