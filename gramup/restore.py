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

from shutil import copyfile,rmtree
from os.path import join,dirname,isfile
from os import makedirs
try :
	from constants import RE_FOLDER,MESGS_DIR,OTHER_FOLDER
	from utils import print_progress_bar,get_messages,download_file,get_file_id,get_logger
except ImportError :
	from .constants import RE_FOLDER,MESGS_DIR,OTHER_FOLDER
	from .utils import print_progress_bar,get_messages,download_file,get_file_id,get_logger

def download_files(tg_client,chat_id) :
	'''
		This function downloads and moves files to the
		appropriate directories in RE_FOLDER
	'''
	files = get_messages(tg_client,chat_id)
	restored,failed,total = (0,0,len(files))
	errors,file_log = "",get_logger()

	file_log.info("%s files to restore",total)

	if total <= 0 :
		return (0,0,"")

	print_progress_bar(0,total)

	for (msg_id,file_id,path) in files :

		if isfile(join(RE_FOLDER,path)) :
			restored+=1
			print_progress_bar(restored+failed, total, prefix = restored+failed, suffix = f" of {total} done")
			continue

		task = download_file(tg_client,file_id if file_id else get_file_id(tg_client,chat_id,msg_id))

		if not ( path and dirname(path) ):
			path = join(OTHER_FOLDER,str(file_id))

		if task.error_info is None :
			makedirs(dirname(join(RE_FOLDER,path)), exist_ok=True)
			copyfile(task.update["local"]["path"],join(RE_FOLDER,path))
			restored += 1
		else :
			file_log.error("Error restoring file %s",task.error_info)
			errors += str(task.error_info) + "\n"
			failed += 1

		print_progress_bar(restored+failed, total, prefix = restored+failed, suffix = f" of {total} done")

	return (restored,failed,errors)

def restore(tg_client_client,chat_id) :
	'''
		This function starts the restore process.
	'''
	print("Restoring files\nPress ctrl+c to save progress and stop.\n")
	(restored,failed,errors) = download_files(tg_client_client,chat_id)

	print("\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
	print(f"{restored} files restored to ~/Restored")
	print(f"{failed} failed \n")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

	try :
		rmtree(MESGS_DIR)
	except FileNotFoundError :
		get_logger().error("Messages directory not found.")

	if failed > 0 and input("Do you wan't to see the error log (y/N) ? : ").lower() == "y" :
		print(errors)

	input("Press enter to continue.")
