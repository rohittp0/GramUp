from login import login
from backup import backup
from restore import restore

def clientReady(tg,chat_id,bup_folders) :
	choise = input("Backup (b) or Restore (r) ? : ")        
	
	if choise == "b" :
		backup(tg,chat_id,bup_folders)
	elif choise == "r" :
		restore(tg,chat_id)
		
	print("Invalid option")
    		    
if __name__ == "__main__" :
	login(clientReady)    

