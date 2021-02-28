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

try:
	import sys
	from login import login
	from backup import backup
	from search import search
	from restore import restore
	from __init__ import __version__
except ImportError:
	from .login import login
	from .backup import backup
	from .search import search
	from .restore import restore
	from .__init__ import VERSION

def client_ready(tg_client,chat_id,bup_folders) :
	'''
		This function is called once required data is
		loaded and Telegram client is initalised.
	'''
	if not ( tg_client or chat_id or bup_folders ) :
		sys.exit()(3)

	choise = None
	try:
		while choise != "q" :

			print("\n======= Menu =======")
			print("  (b) Backup\n  (r) Restore\n  (s) Search\n  (q) Quit\n")
			choise = input("Select an option : ").lower()

			if choise == "b" :
				backup(tg_client,chat_id,bup_folders)
			elif choise == "r" :
				restore(tg_client,chat_id)
			elif choise == "s" :
				search(tg_client,chat_id)
			elif choise != "q" :
				print("Invalid option")
	except KeyboardInterrupt :
		print("\n\nExiting...")
	sys.exit(0)

def main() :
	'''
		This function is called to start GramUp.
	'''
	banner = [
		"\n\n"
		f"   █████████                                      █████  █████  v{VERSION}",
		"  ███░░░░░███                                    ░░███  ░░███",
		" ███     ░░░  ████████   ██████   █████████████   ░███   ░███  ████████",
		"░███         ░░███░░███ ░░░░░███ ░░███░░███░░███  ░███   ░███ ░░███░░███",
		"░███    █████ ░███ ░░░   ███████  ░███ ░███ ░███  ░███   ░███  ░███ ░███",
		"░░███  ░░███  ░███      ███░░███  ░███ ░███ ░███  ░███   ░███  ░███ ░███",
		" ░░█████████  █████    ░░████████ █████░███ █████ ░░████████   ░███████",
		"  ░░░░░░░░░  ░░░░░      ░░░░░░░░ ░░░░░ ░░░ ░░░░░   ░░░░░░░░    ░███░░░",
		"                                                               ░███",
		"                          KEEP YOUR FILES SAFE                 █████",
		"                                                              ░░░░░\n\n"
	]
	for line in banner :
		print(line)

	login(client_ready)

if __name__ == "__main__" :
	main()
