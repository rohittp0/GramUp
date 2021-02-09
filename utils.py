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
		
