# Load data
This function tries to read phone number, chat id and list of backup 
folders from DATA_FILE. If they are not found it prompts user to enter them.
## Returns
Returns the following tuple (phone_number, chat_id, backup_folders)
 - phone_number : (str) Phone number of the user
 
 - chat_id : (int) Chat id of the chat to be used for backup
 
 - backup_folders : (list) List of folders to be backed up
