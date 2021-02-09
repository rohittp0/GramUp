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

from shutil import get_terminal_size
from pathlib import Path
import pickle

def getNewFiles(root,old_files) : 
	files = set([])
	grandparent = Path(root).parent
	
	for path in Path(root).rglob('*') :
		if path.is_file() :
			files.add(str(path))
		
	return [(item,grandparent) for item in files - old_files]	

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', autosize = False):
	"""
	Call in a loop to create terminal progress bar
	@params:
		iteration   - Required  : current iteration (Int)
		total	   - Required  : total iterations (Int)
		prefix	  - Optional  : prefix string (Str)
		suffix	  - Optional  : suffix string (Str)
		decimals	- Optional  : positive number of decimals in percent complete (Int)
		length	  - Optional  : character length of bar (Int)
		fill		- Optional  : bar fill character (Str)
		autosize	- Optional  : automatically resize the length of the progress bar to the terminal window (Bool)
	"""
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	styling = '%s |%s| %s%% %s' % (prefix, fill, percent, suffix)
	if autosize:
		cols, _ = get_terminal_size(fallback = (length, 1))
		length = cols - len(styling)
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print('\r%s' % styling.replace(fill, bar), end = '\r')
	# Print New Line on Complete
	if iteration == total: 
		print()		
		
