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

try:
	from login import login
	from backup import backup
	from restore import restore
	from __init__ import __version__
except : 	
	from .login import login
	from .backup import backup
	from .restore import restore
	from .__init__ import __version__

def clientReady(tg,chat_id,bup_folders) :
	choise = input("Backup (b) or Restore (r) ? : ")        
	
	if choise == "b" :
		backup(tg,chat_id,bup_folders)
	elif choise == "r" :
		restore(tg,chat_id)
	else :
		print("Invalid option")

def main() :
	banner = [
		f"\n\n"
		f"   █████████                                      █████  █████  v{__version__}",      
		f"  ███░░░░░███                                    ░░███  ░░███",
		f" ███     ░░░  ████████   ██████   █████████████   ░███   ░███  ████████",
		f"░███         ░░███░░███ ░░░░░███ ░░███░░███░░███  ░███   ░███ ░░███░░███",
		f"░███    █████ ░███ ░░░   ███████  ░███ ░███ ░███  ░███   ░███  ░███ ░███",
		f"░░███  ░░███  ░███      ███░░███  ░███ ░███ ░███  ░███   ░███  ░███ ░███",
		f" ░░█████████  █████    ░░████████ █████░███ █████ ░░████████   ░███████", 
		f"  ░░░░░░░░░  ░░░░░      ░░░░░░░░ ░░░░░ ░░░ ░░░░░   ░░░░░░░░    ░███░░░",  
		f"                                                               ░███",     
		f"                          KEEP YOUR FILES SAFE                 █████",    
		f"                                                              ░░░░░\n\n"
	]
	for line in banner : 
		print(line)
	
	login(clientReady)	
    		    
if __name__ == "__main__" :
	main()   

