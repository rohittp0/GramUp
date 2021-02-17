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

from shutil import get_terminal_size
from pathlib import Path

def get_messages(tg_client,chat_id) :
	'''
		This function gets all messages from a chat.
	'''
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
		if not "messages" in messages.update or not len(messages.update["messages"]) > 0  :
			break

		for message in messages.update["messages"] :
			if "document" in message["content"] :
				if message["content"]["document"]["document"]["remote"]["is_uploading_completed"] :
					yield (
						message["content"]["document"]["document"]["local"]["id"],
						message["content"]["caption"]["text"]
					)

		last_id = messages.update["messages"][-1]["id"]

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
